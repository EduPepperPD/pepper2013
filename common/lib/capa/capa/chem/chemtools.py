from collections import OrderedDict
import json
import unittest


def vsepr_parse_user_answer(user_input):
    d = OrderedDict(json.loads(user_input))
    d['atoms'] = OrderedDict(sorted(d['atoms'].items()))
    return d


def vsepr_build_correct_answer(geometry, atoms):
    correct_answer = OrderedDict()
    correct_answer['geometry'] = geometry
    correct_answer['atoms'] = OrderedDict(sorted(atoms.items()))
    return correct_answer


def vsepr_grade(user_input, correct_answer, ignore_p_order=False, ignore_a_order=False, ignore_e_order=False):
    """ Flags ignore_(a,p,e)_order are for checking order in axial, perepherial or equatorial positions.
        Allowed cases:
            c0, a, e
            c0, p
        Not implemented and not tested cases when p with a or e (no need for now)
    """
    # print user_input, type(user_input)
    # print correct_answer, type(correct_answer)
    if user_input['geometry'] != correct_answer['geometry']:
        return False

    if user_input['atoms']['c0'] != correct_answer['atoms']['c0']:
        return False

    # not order-aware comparisons
    for ignore in [(ignore_p_order, 'p'), (ignore_e_order, 'e'), (ignore_a_order, 'a')]:
        if ignore[0]:
            # collecting atoms:
            a_user = [v for k, v in user_input['atoms'].items() if k.startswith(ignore[1])]
            a_correct = [v for k, v in correct_answer['atoms'].items() if k.startswith(ignore[1])]
            # print ignore[0], ignore[1], a_user, a_correct
            if len(a_user) != len(a_correct):
                return False
            if sorted(a_user) != sorted(a_correct):
                return False

    # order-aware comparisons
    for ignore in [(ignore_p_order, 'p'), (ignore_e_order, 'e'), (ignore_a_order, 'a')]:
        if not ignore[0]:
            # collecting atoms:
            a_user = [v for k, v in user_input['atoms'].items() if k.startswith(ignore[1])]
            a_correct = [v for k, v in correct_answer['atoms'].items() if k.startswith(ignore[1])]
            # print '2nd', ignore[0], ignore[1], a_user, a_correct
            if len(a_user) != len(a_correct):
                return False
            if len(a_correct) == 0:
                continue
            if a_user != a_correct:
                return False

    return True


class Test_Grade(unittest.TestCase):
    ''' test grade function '''

    def test_incorrect_geometry(self):
        correct_answer = vsepr_build_correct_answer(geometry="AX4E0", atoms={"c0": "N", "p0": "H", "p1": "(ep)", "p2": "H", "p3": "H"})
        user_answer = vsepr_parse_user_answer(u'{"geometry":"AX3E0","atoms":{"c0":"B","p0":"F","p1":"B","p2":"F"}}')
        self.assertFalse(vsepr_grade(user_answer, correct_answer))

    def test_incorrect_positions(self):
        correct_answer = vsepr_build_correct_answer(geometry="AX4E0", atoms={"c0": "N", "p0": "H", "p1": "(ep)", "p2": "H", "p3": "H"})
        user_answer = vsepr_parse_user_answer(u'{"geometry":"AX4E0","atoms":{"c0":"B","p0":"F","p1":"B","p2":"F"}}')
        self.assertFalse(vsepr_grade(user_answer, correct_answer))

    def test_correct_answer(self):
        correct_answer = vsepr_build_correct_answer(geometry="AX4E0", atoms={"c0": "N", "p0": "H", "p1": "(ep)", "p2": "H", "p3": "H"})
        user_answer = vsepr_parse_user_answer(u'{"geometry":"AX4E0","atoms":{"c0":"N","p0":"H","p1":"(ep)","p2":"H", "p3":"H"}}')
        self.assertTrue(vsepr_grade(user_answer, correct_answer))

    def test_incorrect_position_order_p(self):
        correct_answer = vsepr_build_correct_answer(geometry="AX4E0", atoms={"c0": "N", "p0": "H", "p1": "(ep)", "p2": "H", "p3": "H"})
        user_answer = vsepr_parse_user_answer(u'{"geometry":"AX4E0","atoms":{"c0":"N","p0":"H","p1":"H","p2":"(ep)", "p3":"H"}}')
        self.assertFalse(vsepr_grade(user_answer, correct_answer))

    def test_correct_position_order_with_ignore_p_order(self):
        correct_answer = vsepr_build_correct_answer(geometry="AX4E0", atoms={"c0": "N", "p0": "H", "p1": "(ep)", "p2": "H", "p3": "H"})
        user_answer = vsepr_parse_user_answer(u'{"geometry":"AX4E0","atoms":{"c0":"N","p0":"H","p1":"H","p2":"(ep)", "p3":"H"}}')
        self.assertTrue(vsepr_grade(user_answer, correct_answer, ignore_p_order=True))

    def test_incorrect_position_order_ae(self):
        correct_answer = vsepr_build_correct_answer(geometry="AX6E0", atoms={"c0": "Br", "a0": "test", "a1": "(ep)", "e0": "H", "e1": "H", "e2": "(ep)", "e3": "(ep)"})
        user_answer = vsepr_parse_user_answer(u'{"geometry":"AX6E0","atoms":{"c0":"Br","a0":"test","a1":"(ep)","e0":"H","e1":"(ep)","e2":"(ep)","e3":"(ep)"}}')
        self.assertFalse(vsepr_grade(user_answer, correct_answer))

    def test_correct_position_order_with_ignore_a_order_not_e(self):
        correct_answer = vsepr_build_correct_answer(geometry="AX6E0", atoms={"c0": "Br", "a0": "(ep)", "a1": "test", "e0": "H", "e1": "H", "e2": "(ep)", "e3": "(ep)"})
        user_answer = vsepr_parse_user_answer(u'{"geometry":"AX6E0","atoms":{"c0":"Br","a0":"test","a1":"(ep)","e0":"H","e1":"H","e2":"(ep)","e3":"(ep)"}}')
        self.assertTrue(vsepr_grade(user_answer, correct_answer, ignore_a_order=True))

    def test_incorrect_position_order_with_ignore_a_order_not_e(self):
        correct_answer = vsepr_build_correct_answer(geometry="AX6E0", atoms={"c0": "Br", "a0": "(ep)", "a1": "test", "e0": "H", "e1": "H", "e2": "H", "e3": "(ep)"})
        user_answer = vsepr_parse_user_answer(u'{"geometry":"AX6E0","atoms":{"c0":"Br","a0":"test","a1":"(ep)","e0":"H","e1":"H","e2":"(ep)","e3":"H"}}')
        self.assertFalse(vsepr_grade(user_answer, correct_answer, ignore_a_order=True))

    def test_correct_position_order_with_ignore_e_order_not_a(self):
        correct_answer = vsepr_build_correct_answer(geometry="AX6E0", atoms={"c0": "Br", "a0": "(ep)", "a1": "test", "e0": "H", "e1": "H", "e2": "H", "e3": "(ep)"})
        user_answer = vsepr_parse_user_answer(u'{"geometry":"AX6E0","atoms":{"c0":"Br","a0":"(ep)","a1":"test","e0":"H","e1":"H","e2":"(ep)","e3":"H"}}')
        self.assertTrue(vsepr_grade(user_answer, correct_answer, ignore_e_order=True))

    def test_incorrect_position_order_with_ignore_e_order__not_a(self):
        correct_answer = vsepr_build_correct_answer(geometry="AX6E0", atoms={"c0": "Br", "a0": "(ep)", "a1": "test", "e0": "H", "e1": "H", "e2": "H", "e3": "(ep)"})
        user_answer = vsepr_parse_user_answer(u'{"geometry":"AX6E0","atoms":{"c0":"Br","a0":"test","a1":"(ep)","e0":"H","e1":"H","e2":"(ep)","e3":"H"}}')
        self.assertFalse(vsepr_grade(user_answer, correct_answer, ignore_e_order=True))

    def test_correct_position_order_with_ignore_ae_order(self):
        correct_answer = vsepr_build_correct_answer(geometry="AX6E0", atoms={"c0": "Br", "a0": "(ep)", "a1": "test", "e0": "H", "e1": "H", "e2": "H", "e3": "(ep)"})
        user_answer = vsepr_parse_user_answer(u'{"geometry":"AX6E0","atoms":{"c0":"Br","a0":"test","a1":"(ep)","e0":"H","e1":"H","e2":"(ep)","e3":"H"}}')
        self.assertTrue(vsepr_grade(user_answer, correct_answer, ignore_e_order=True, ignore_a_order=True))

    def test_incorrect_c0(self):
        correct_answer = vsepr_build_correct_answer(geometry="AX6E0", atoms={"c0": "Br", "a0": "(ep)", "a1": "test", "e0": "H", "e1": "H", "e2": "H", "e3": "(ep)"})
        user_answer = vsepr_parse_user_answer(u'{"geometry":"AX6E0","atoms":{"c0":"H","a0":"test","a1":"(ep)","e0":"H","e1":"H","e2":"(ep)","e3":"H"}}')
        self.assertFalse(vsepr_grade(user_answer, correct_answer, ignore_e_order=True, ignore_a_order=True))


def suite():

    testcases = [Test_Grade]
    suites = []
    for testcase in testcases:
        suites.append(unittest.TestLoader().loadTestsFromTestCase(testcase))
    return unittest.TestSuite(suites)

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())