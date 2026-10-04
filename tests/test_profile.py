import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / 'plugins/personal-intelligence/skills/setup-personal-intelligence/scripts/profile_tools.py'
spec = importlib.util.spec_from_file_location('profile_tools', HELPER)
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)

class ProfileTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / 'examples/synthetic'
        self.req = json.loads((base / 'requirements.json').read_text())
        self.profile = json.loads((base / 'profile.json').read_text())
        self.mapping = json.loads((base / 'local-map.json').read_text())
        # Every negative case starts from a verified valid independent baseline.
        api.validate(self.req,self.profile,self.mapping)

    def request(self, domain='health', intent='baseline', subject='patient_a', **extra):
        return dict(domain=domain, intent=intent, subject=subject, qualifiers={'topic_ref':'fixture:observation'}, **extra)

    def rejects(self, profile=None, req=None, mapping=None):
        with self.assertRaises(api.ProfileError):
            api.validate(self.req if req is None else req, self.profile if profile is None else profile, self.mapping if mapping is None else mapping)

    def test_fresh_private_setup_cli_and_no_mapped_content_access(self):
        with tempfile.TemporaryDirectory() as directory:
            os.chmod(directory, 0o700)
            private = Path(directory)
            for name, data in [('requirements',self.req),('profile',self.profile),('local-map',self.mapping)]:
                target = private / (name+'.json'); target.write_text(json.dumps(data)); os.chmod(target,0o600)
            command = [sys.executable,str(HELPER),'validate','--requirements',str(private/'requirements.json'),'--profile',str(private/'profile.json'),'--local-map',str(private/'local-map.json')]
            result = subprocess.run(command,capture_output=True,text=True,check=True)
            output = json.loads(result.stdout)
            self.assertEqual(output['status'],'PASS')
            self.assertEqual((output['content_reads'],output['provider_calls']),(0,0))
            self.assertEqual((output['routes'],output['labels']),(9,4))
            self.assertFalse((private/'health.patient_a.baseline').exists())

    def test_cli_plan_revalidates_independent_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            private=Path(directory)
            for name,data in [('requirements',self.req),('profile',self.profile),('local-map',self.mapping),('request',self.request())]:
                (private/(name+'.json')).write_text(json.dumps(data))
            command=[sys.executable,str(HELPER),'plan']
            for name in ['requirements','profile','local-map','request']:
                command+=['--'+name,str(private/(name+'.json'))]
            result=subprocess.run(command,text=True,capture_output=True,check=True)
            self.assertEqual(json.loads(result.stdout)['route_id'],'health-baseline-a')
            altered=copy.deepcopy(self.req);altered['priority_labels'].pop()
            (private/'requirements.json').write_text(json.dumps(altered))
            result=subprocess.run(command,text=True,capture_output=True)
            self.assertEqual(result.returncode,1)
            self.assertEqual(json.loads(result.stdout)['code'],'requirements_digest_mismatch')

    def test_each_priority_label_omission_rejected_even_if_route_label_cleared(self):
        for label in self.profile['labels']:
            with self.subTest(label=label['id']):
                p=copy.deepcopy(self.profile)
                p['labels']=[entry for entry in p['labels'] if entry['id']!=label['id']]
                for r in p['routes']:
                    if r['label_id']==label['id']:r['label_id']=None
                self.rejects(profile=p)

    def test_changed_label_exact_name_rejected(self):
        self.profile['labels'][0]['name']='Different Archive';self.rejects()

    def test_independent_requirement_drift_rejected(self):
        self.req['priority_labels'].pop();self.rejects()

    def test_missing_source_or_capability_rejected(self):
        p=copy.deepcopy(self.profile);p['sources'].pop();self.rejects(profile=p)
        p=copy.deepcopy(self.profile);p['routes'].pop();self.rejects(profile=p)

    def test_extra_unconfirmed_source_rejected(self):
        extra=copy.deepcopy(self.profile['sources'][0]);extra['id']='health.unconfirmed';extra['location_ref']=extra['id'];self.profile['sources'].append(extra);self.rejects()

    def test_changed_authority_rejected(self):
        self.profile['sources'][0]['role']='derived';self.rejects()

    def test_cross_patient_route_rejected(self):
        self.profile['routes'][0]['source_ids']=['health.patient_b.baseline'];self.rejects()

    def test_separate_patients_have_separate_routes(self):
        for patient in ['patient_a','patient_b']:
            answer=api.plan(self.profile,self.request(subject=patient))
            self.assertEqual(answer['source_ids'],['health.'+patient+'.baseline'])
            self.assertFalse(answer['authorization_established'])

    def test_multiple_or_missing_patients_do_not_select_route(self):
        for subject in [['patient_a','patient_b'],None,'*']:
            self.assertEqual(api.plan(self.profile,self.request(subject=subject))['status'],'needs_single_subject')

    def test_finance_requires_human_flag_and_scope(self):
        q=self.request('finance','balance','household')
        self.assertEqual(api.plan(self.profile,q)['status'],'excluded_finance')
        q['explicit_financial_question']=True
        self.assertEqual(api.plan(self.profile,q)['status'],'needs_qualifier')
        q['qualifiers']={'account_ref':'all-recorded-accounts','topic_ref':'fixture:balance','date_range':'2030-02'}
        result=api.plan(self.profile,q)
        self.assertEqual(result['status'],'source_readiness_unverified')
        self.assertNotIn('balance',result)

    def test_weakening_finance_scope_rejected(self):
        self.profile['routes'][-1]['required_qualifiers']=['topic_ref'];self.rejects()

    def test_sensitive_source_cannot_route_through_generic_domain(self):
        self.profile['routes'][-1]['domain']='administration';self.rejects()

    def test_label_spaces_preserved_without_claiming_live_access(self):
        q=self.request('travel','booking','household')
        q['qualifiers']={'trip_ref':'fixture:stay','booking_ref':'fixture:confirmation'}
        answer=api.plan(self.profile,q)
        self.assertEqual(answer['initial_query'],'label:"Journeys Archive"')
        self.assertEqual(answer['status'],'source_readiness_unverified')
        self.assertEqual(answer['provider_calls'],0)

    def test_label_injection_rejected(self):
        for name in ['Archive" OR in:anywhere','Archive\\Inbox','Archive\nOther','*']:
            p=copy.deepcopy(self.profile);p['labels'][0]['name']=name
            with self.subTest(name=name):self.rejects(profile=p)

    def test_label_cannot_select_another_route(self):
        q=self.request();q['label_id']='receipts'
        self.assertEqual(api.plan(self.profile,q)['status'],'label_route_mismatch')

    def test_source_path_and_request_overrides_rejected(self):
        for key in ['requested_source_ids','path','command','content_class']:
            q=self.request();q[key]='fixture:override'
            self.assertEqual(api.plan(self.profile,q)['status'],'request_override_or_unknown_field_rejected')

    def test_map_completeness_and_instruction_references(self):
        self.mapping['mappings'].pop();self.rejects()
        self.setUp()
        self.profile['sources'][0]['instruction_refs']=['guide.health']
        self.rejects()
        self.mapping['mappings'][0]['instructions']={'guide.health':'synthetic://instruction'}
        self.assertEqual(api.validate(self.req,self.profile,self.mapping)['status'],'PASS')

    def test_mapping_locations_are_not_opened(self):
        for entry in self.mapping['mappings']:entry['location']='synthetic://intentionally-nonexistent'
        self.assertEqual(api.validate(self.req,self.profile,self.mapping)['content_reads'],0)

    def test_empty_templates_are_not_a_complete_setup(self):
        base=HELPER.parents[1]/'assets'
        req=json.loads((base/'requirements.template.json').read_text())
        p=json.loads((base/'profile.template.json').read_text());p['requirements_sha256']=api.fingerprint(req)
        m=json.loads((base/'local-map.template.json').read_text())
        self.rejects(profile=p,req=req,mapping=m)

    def test_duplicate_json_keys_rejected_without_value_disclosure(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'input.json';path.write_text('{"id":"first","id":"sensitive-demo-value"}')
            with self.assertRaisesRegex(api.ProfileError,'^duplicate_json_key$'):api.load_metadata(path)

    def test_cli_failure_does_not_echo_private_path_or_values(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'sensitive-demo-filename.json';path.write_text('sensitive-demo-value')
            result=subprocess.run([sys.executable,str(HELPER),'fingerprint','--requirements',str(path)],text=True,capture_output=True)
            self.assertEqual(result.returncode,1)
            self.assertNotIn('sensitive-demo',result.stdout+result.stderr)
            self.assertEqual(json.loads(result.stdout)['code'],'metadata_unreadable_or_invalid_json')

    def test_unknown_profile_field_does_not_create_capability(self):
        self.profile['shell_command']='fixture:command';self.rejects()

    def test_general_retrieval_or_fallback_cannot_be_enabled(self):
        self.profile['general_retrieval_enabled']=True;self.rejects()
        self.setUp();self.profile['policy']['automatic_fallback']=True;self.rejects()

    def test_invalid_confirmation_date_rejected(self):
        self.req['input_basis']['confirmed_at']='next week'
        self.profile['requirements_sha256']=api.fingerprint(self.req)
        self.rejects()

    def test_false_integer_not_a_policy_boolean(self):
        self.profile['policy']['automatic_fallback']=0;self.rejects()

    def test_schema_bool_not_accepted_as_integer(self):
        self.profile['schema_version']=True;self.rejects()

if __name__=='__main__':unittest.main()
