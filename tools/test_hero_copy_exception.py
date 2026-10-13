"""Regression tests for the exact heading exception; no network or Webflow calls."""
import copy
import unittest
from hero_copy_exception import prepare_for_baseline, H1, TEXTS, ORIGINALS, LIMITS, ELEMENTS, COMPONENT, EXCEPTION_ID

class ExactHeroTests(unittest.TestCase):
    def setUp(self):
        self.row = {'id': 'HOME-003', 'action': 'rewrite', 'new_text': H1, 'max_chars': 50,
                    'validation_exception': EXCEPTION_ID, 'claim_evidence': 'evidence.md#p1', 'layout_review': 'pending',
                    'new_segments': [{'source_id': {'component': COMPONENT, 'element': el}, 'original_raw': orig,
                                      'max_chars': limit, 'new_text': txt} for el, orig, limit, txt in zip(ELEMENTS, ORIGINALS, LIMITS, TEXTS)]}
        self.policy = {'exception_id': EXCEPTION_ID, 'field_id': 'HOME-003', 'approved_text': H1, 'segments': TEXTS,
                       'original_segment_max_chars': LIMITS, 'replacement_segment_lengths': [10, 7, 13, 8],
                       'original_total_max_chars': 50, 'new_total_chars': 41, 'visual_acceptance': 'pending'}
    def run_case(self):
        return prepare_for_baseline({'items': [self.row]}, self.policy)
    def test_exact_copy_and_disclosure(self):
        original = copy.deepcopy(self.row)
        candidate, exceptions, errors = self.run_case()
        self.assertFalse(errors)
        self.assertEqual(exceptions[0]['field_id'], 'HOME-003')
        self.assertEqual(candidate['items'][0]['action'], 'keep')
        self.assertEqual(self.row, original)
    def test_no_general_exception(self):
        self.row['id'] = 'HOME-004'
        self.assertTrue(self.run_case()[2])
    def test_changed_approved_text_rejected(self):
        self.row['new_text'] += ' with AI'
        self.assertTrue(self.run_case()[2])
    def test_original_budget_cannot_be_enlarged(self):
        self.row['max_chars'] = 60
        self.assertTrue(self.run_case()[2])
    def test_segment_budget_cannot_be_rewritten(self):
        self.row['new_segments'][0]['max_chars'] = 10
        self.assertTrue(self.run_case()[2])
    def test_ids_preserved(self):
        self.row['new_segments'][0]['source_id']['element'] = 'invented'
        self.assertTrue(self.run_case()[2])
    def test_boundary_spaces_preserved(self):
        self.row['new_segments'][0]['new_text'] = 'Enterprise'
        self.assertTrue(self.run_case()[2])
    def test_missing_node_rejected(self):
        self.row['new_segments'].pop()
        self.assertTrue(self.run_case()[2])
    def test_policy_tampering_rejected(self):
        self.policy['new_total_chars'] = 99
        self.assertTrue(self.run_case()[2])
    def test_unmarked_copy_uses_frozen_validation(self):
        self.row.pop('validation_exception')
        data = {'items': [self.row]}
        candidate, exceptions, errors = prepare_for_baseline(data, self.policy)
        self.assertIs(candidate, data)
        self.assertFalse(exceptions)
        self.assertFalse(errors)
    def test_unrelated_field_not_sanitized(self):
        other = {'id': 'HOME-004', 'action': 'rewrite', 'new_text': 'X' * 500}
        candidate, _, errors = prepare_for_baseline({'items': [self.row, other]}, self.policy)
        self.assertFalse(errors)
        self.assertEqual(candidate['items'][1], other)
    def test_visual_approval_not_invented(self):
        self.row['layout_review'] = 'passed'
        self.assertTrue(self.run_case()[2])

if __name__ == '__main__':
    unittest.main()
