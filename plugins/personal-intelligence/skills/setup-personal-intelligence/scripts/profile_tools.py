#!/usr/bin/env python3
"""Offline metadata validation/planning. No mapped content or provider reads."""
import argparse
from datetime import date, datetime
import hashlib
import json
import re
from pathlib import Path
ID = re.compile(r'^[a-z][a-z0-9._-]{0,100}$')
ROLES = {'live', 'canonical', 'original', 'derived', 'archive'}
FRESHNESS = {'live', 'dated', 'historical'}

class ProfileError(ValueError):
    pass

def need(ok, code):
    if not ok:
        raise ProfileError(code)

def obj(v, keys, code):
    need(isinstance(v, dict) and set(v) == set(keys), code)

def text(v):
    return isinstance(v, str) and bool(v.strip()) and '*' not in v and not any(ord(c) < 32 for c in v)

def ids(v):
    return isinstance(v, list) and all(isinstance(x, str) and ID.fullmatch(x) for x in v) and len(set(v)) == len(v)

def index(items, code):
    need(isinstance(items, list), code)
    result = {}
    for item in items:
        need(isinstance(item, dict) and isinstance(item.get('id'), str) and ID.fullmatch(item['id']), code)
        need(item['id'] not in result, code + '_duplicate')
        result[item['id']] = item
    return result

def fingerprint(requirements):
    return hashlib.sha256(json.dumps(requirements, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()

def duplicate_safe(pairs):
    d = {}
    for k, v in pairs:
        need(k not in d, 'duplicate_json_key')
        d[k] = v
    return d

def load_metadata(path):
    # Opens only this explicit metadata file, never the locations it contains.
    p = Path(path)
    need(p.is_file() and p.stat().st_size <= 2_000_000, 'metadata_file_unavailable_or_too_large')
    try:
        return json.loads(p.read_text(), object_pairs_hook=duplicate_safe)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ProfileError('metadata_unreadable_or_invalid_json') from exc

def profile_structure(p):
    obj(p, ['schema_version', 'requirements_sha256', 'general_retrieval_enabled', 'policy', 'integrations', 'sources', 'routes', 'labels'], 'profile_keys')
    need(type(p['schema_version']) is int and p['schema_version'] == 1, 'profile_schema')
    need(p['general_retrieval_enabled'] is False, 'general_retrieval_must_remain_disabled')
    need(isinstance(p['requirements_sha256'], str) and re.fullmatch('[a-f0-9]{64}', p['requirements_sha256']), 'requirement_digest_format')
    need(p['policy'] == {'finance': 'explicit_question_only', 'identity': 'task_specific_need', 'email': 'designated_provider_only', 'automatic_fallback': False} and p['policy']['automatic_fallback'] is False, 'policy_boundary_changed')
    integrations = index(p['integrations'], 'integrations')
    for i in integrations.values():
        obj(i, ['id', 'kind', 'provider', 'readiness'], 'integration_keys')
        need(i['kind'] in {'local_files', 'provider'} and text(i['provider']) and i['readiness'] in {'unverified', 'user_confirmed', 'verified'}, 'integration_metadata')
    sources = index(p['sources'], 'sources')
    need(bool(sources), 'sources_empty')
    for s in sources.values():
        obj(s, ['id', 'domain', 'subjects', 'role', 'kind', 'integration_id', 'location_ref', 'instruction_refs'], 'source_keys')
        need(text(s['domain']) and ids(s['subjects']) and bool(s['subjects']) and s['role'] in ROLES and s['kind'] in {'file', 'email', 'ledger', 'service'} and ids(s['instruction_refs']), 'source_metadata')
        need(s['integration_id'] in integrations, 'source_integration_missing')
        i = integrations[s['integration_id']]
        if s['kind'] == 'file':
            need(i['kind'] == 'local_files' and s['location_ref'] == s['id'], 'file_source_location_contract')
            if s['domain'] == 'health':
                need(len(s['subjects']) == 1, 'local_clinical_source_requires_one_patient')
        else:
            need(i['kind'] == 'provider' and s['location_ref'] is None and s['instruction_refs'] == [], 'provider_source_contract')
        if s['kind'] == 'ledger':
            need(s['domain'] == 'finance', 'ledger_requires_finance_domain')
    routes = index(p['routes'], 'routes')
    need(bool(routes), 'routes_empty')
    combinations = set()
    for r in routes.values():
        obj(r, ['id', 'domain', 'intent', 'subject', 'source_ids', 'required_qualifiers', 'freshness', 'label_id'], 'route_keys')
        need(all(text(r[k]) for k in ['domain', 'intent', 'subject']) and ids(r['source_ids']) and bool(r['source_ids']) and ids(r['required_qualifiers']) and r['freshness'] in FRESHNESS, 'route_metadata')
        c = tuple(r[k] for k in ['domain', 'intent', 'subject'])
        need(c not in combinations, 'ambiguous_route'); combinations.add(c)
        need(all(sid in sources for sid in r['source_ids']), 'route_source_missing')
        need(all(r['subject'] in sources[sid]['subjects'] for sid in r['source_ids']), 'route_subject_mismatch')
        need(all(sources[sid]['domain'] not in {'finance', 'health', 'identity'} or sources[sid]['domain'] == r['domain'] for sid in r['source_ids']), 'sensitive_source_domain_mismatch')
        if r['domain'] == 'finance':
            need({'account_ref', 'topic_ref', 'date_range'} <= set(r['required_qualifiers']), 'finance_scope_missing')
        if r['domain'] == 'identity':
            need('field_set' in r['required_qualifiers'], 'identity_field_scope_missing')
        if r['subject'] == 'owner_private':
            need('owner_ref' in r['required_qualifiers'], 'owner_scope_missing')
        need(r['label_id'] is None or isinstance(r['label_id'], str), 'route_label_format')
    labels = index(p['labels'], 'labels'); names = set()
    for l in labels.values():
        obj(l, ['id', 'name', 'source_id', 'route_id', 'coverage'], 'label_keys')
        name = l['name']
        need(text(name) and not any(c in name for c in ['"', '\\']) and name not in names, 'unsafe_or_duplicate_label_name'); names.add(name)
        need(l['coverage'] in {'unknown', 'all_confirmations'}, 'label_coverage')
        need(l['source_id'] in sources and l['route_id'] in routes, 'label_source_or_route_missing')
        s = sources[l['source_id']]; r = routes[l['route_id']]
        need(s['kind'] == 'email' and integrations[s['integration_id']]['provider'] == 'gmail', 'label_requires_gmail_provider')
        need(l['source_id'] in r['source_ids'] and r['label_id'] == l['id'], 'label_route_binding')
    need(all(r['label_id'] is None or r['label_id'] in labels for r in routes.values()), 'route_label_missing')
    return sources, routes, labels, integrations

def validate(req, p, m):
    obj(req, ['schema_version', 'input_basis', 'source_requirements', 'capability_requirements', 'priority_labels'], 'requirements_keys')
    need(type(req['schema_version']) is int and req['schema_version'] == 1, 'requirements_schema')
    obj(req['input_basis'], ['kind', 'confirmed_at'], 'input_basis_keys')
    need(req['input_basis']['kind'] in {'synthetic', 'user_confirmation'} and text(req['input_basis']['confirmed_at']), 'input_confirmation_missing')
    try:
        timestamp = req['input_basis']['confirmed_at']
        date.fromisoformat(timestamp) if len(timestamp) == 10 else datetime.fromisoformat(timestamp)
    except ValueError as exc:
        raise ProfileError('input_confirmation_date_invalid') from exc
    need(isinstance(p, dict) and p.get('requirements_sha256') == fingerprint(req), 'requirements_digest_mismatch')
    sources, routes, labels, integrations = profile_structure(p)
    required = index(req['source_requirements'], 'source_requirements'); bindings = set()
    need(bool(required), 'source_requirements_empty')
    for q in required.values():
        obj(q, ['id', 'source_id', 'domain', 'subject', 'role'], 'source_requirement_keys')
        sid = q['source_id']; need(sid in sources, 'required_source_missing'); s = sources[sid]
        need(s['domain'] == q['domain'] and s['role'] == q['role'] and q['subject'] in s['subjects'], 'required_source_authority_or_subject_changed')
        b = (sid, q['subject']); need(b not in bindings, 'duplicate_source_requirement_binding'); bindings.add(b)
    need(bindings == {(sid, subject) for sid, s in sources.items() for subject in s['subjects']}, 'source_requirement_coverage_mismatch')
    required_routes = index(req['capability_requirements'], 'capability_requirements')
    need(bool(required_routes) and set(required_routes) == set(routes), 'capability_requirement_coverage_mismatch')
    for rid, q in required_routes.items():
        obj(q, ['id', 'domain', 'intent', 'subject', 'source_ids', 'required_qualifiers', 'freshness'], 'capability_requirement_keys')
        need(all(routes[rid][k] == v for k, v in q.items()), 'required_capability_changed')
    required_labels = index(req['priority_labels'], 'priority_labels')
    need(set(required_labels) == set(labels), 'priority_label_coverage_mismatch')
    for lid, q in required_labels.items():
        obj(q, ['id', 'name', 'source_id', 'route_id'], 'label_requirement_keys')
        need(all(labels[lid][k] == v for k, v in q.items()), 'required_label_changed')
    obj(m, ['schema_version', 'mappings'], 'map_keys')
    need(type(m['schema_version']) is int and m['schema_version'] == 1 and isinstance(m['mappings'], list), 'map_schema')
    mapped = set()
    for entry in m['mappings']:
        obj(entry, ['source_id', 'location', 'instructions'], 'mapping_keys')
        sid = entry['source_id']
        need(isinstance(sid, str) and sid not in mapped and sid in sources and sources[sid]['kind'] == 'file', 'mapping_source_mismatch')
        need(text(entry['location']) and isinstance(entry['instructions'], dict), 'mapping_location_or_instructions_missing')
        need(set(entry['instructions']) == set(sources[sid]['instruction_refs']) and all(text(v) for v in entry['instructions'].values()), 'mapping_instruction_coverage_mismatch')
        mapped.add(sid)
    need(mapped == {sid for sid, s in sources.items() if s['kind'] == 'file'}, 'map_coverage_mismatch')
    return {'status': 'PASS', 'scope': 'offline_metadata_only', 'source_bindings': len(bindings), 'routes': len(routes), 'labels': len(labels), 'mapped_sources': len(mapped), 'content_reads': 0, 'provider_calls': 0}

def plan(p, request):
    sources, routes, labels, integrations = profile_structure(p)
    need(isinstance(request, dict), 'request_object_required')
    allowed = {'domain', 'intent', 'subject', 'qualifiers', 'explicit_financial_question', 'explicit_identity_need', 'label_id'}
    if set(request) - allowed:
        return {'status': 'request_override_or_unknown_field_rejected'}
    if not text(request.get('subject')):
        return {'status': 'needs_single_subject'}
    if request.get('domain') == 'finance' and request.get('explicit_financial_question') is not True:
        return {'status': 'excluded_finance'}
    if request.get('domain') == 'identity' and request.get('explicit_identity_need') is not True:
        return {'status': 'excluded_identity'}
    matched = [r for r in routes.values() if all(request.get(k) == r[k] for k in ['domain', 'intent', 'subject'])]
    if len(matched) != 1:
        return {'status': 'unsupported_route'}
    r = matched[0]; qualifiers = request.get('qualifiers', {})
    if not isinstance(qualifiers, dict) or not all(text(v) for v in qualifiers.values()):
        return {'status': 'invalid_qualifier'}
    missing = sorted(set(r['required_qualifiers']) - set(qualifiers))
    if missing:
        return {'status': 'needs_qualifier', 'missing': missing}
    label_id = request.get('label_id', r['label_id'])
    if label_id != r['label_id']:
        return {'status': 'label_route_mismatch'}
    unverified = [sid for sid in r['source_ids'] if integrations[sources[sid]['integration_id']]['readiness'] == 'unverified']
    result = {'status': 'source_readiness_unverified' if unverified else 'route_planned', 'route_id': r['id'], 'source_ids': r['source_ids'], 'freshness': r['freshness'], 'content_reads': 0, 'provider_calls': 0, 'authorization_established': False}
    if label_id:
        result['initial_query'] = 'label:"' + labels[label_id]['name'] + '"'
    if unverified:
        result['unverified_source_ids'] = unverified
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__); sub = parser.add_subparsers(dest='operation', required=True)
    f = sub.add_parser('fingerprint'); f.add_argument('--requirements', required=True)
    v = sub.add_parser('validate')
    for name in ['requirements', 'profile', 'local-map']:
        v.add_argument('--' + name, required=True)
    p = sub.add_parser('plan')
    for name in ['requirements', 'profile', 'local-map', 'request']:
        p.add_argument('--' + name, required=True)
    args = parser.parse_args()
    try:
        if args.operation == 'fingerprint':
            print(fingerprint(load_metadata(args.requirements)))
        elif args.operation == 'validate':
            print(json.dumps(validate(load_metadata(args.requirements), load_metadata(args.profile), load_metadata(args.local_map)), indent=2))
        else:
            requirements = load_metadata(args.requirements)
            profile = load_metadata(args.profile)
            validate(requirements, profile, load_metadata(args.local_map))
            print(json.dumps(plan(profile, load_metadata(args.request)), indent=2))
    except (ProfileError, OSError, TypeError, KeyError) as exc:
        # Never echo private metadata, scope values or paths in errors.
        print(json.dumps({'status': 'FAIL', 'code': str(exc) if isinstance(exc, ProfileError) else 'malformed_or_unreadable_metadata'}))
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
