from django.test import TestCase
from mock import Mock, patch
from referral_system.models import SmsFac

class TestSmsFac(TestCase):
    def setUp(self):
        self.sms_fac_1 = SmsFac(quest_20='facility1', quest_25='2', quest_17='street', quest_19='village',
                                quest_14='commune', quest_31='district', quest_16='province', quest_13='phone',
                                quest_27='phone-1st', quest_32='phone_2', quest_49='hours', quest_28='fp-service',
                                quest_29='safe-abortion', quest_38='safe-abortion-12', quest_21='id13',
                                quest_42='prov-khmer', quest_48='dist-khmer', quest_40='com-khmer',
                                quest_44='village-khmer', quest_35='street-khmer', quest_12='name-khmer')

        self.sms_fac_2 = SmsFac(quest_20='facility2', quest_25='', quest_17='street', quest_19='village',
                                quest_14='commune', quest_31='district', quest_16='province', quest_13='phone',
                                quest_27='phone-1st', quest_32='phone_2', quest_49='hours', quest_28='fp-service',
                                quest_29='safe-abortion', quest_38='safe-abortion-12', quest_21='id13',
                                quest_42='prov-khmer', quest_48='dist-khmer', quest_40='com-khmer',
                                quest_44='village-khmer', quest_35='street-khmer', quest_12='name-khmer')

        self.sms_fac_3 = SmsFac(quest_20='facility3', quest_25='2', quest_17='street', quest_19='village',
                                quest_14='commune', quest_31='district', quest_16='province', quest_13='phone',
                                quest_27='phone-1st', quest_32='phone_2', quest_49='hours', quest_28='fp-service',
                                quest_29='safe-abortion', quest_38='safe-abortion-12', quest_21='id13',
                                quest_42='prov-khmer', quest_48='dist-khmer', quest_40='com-khmer',
                                quest_44='village-khmer', quest_35='street-khmer', quest_12='name-khmer')

    def test_facility_marker(self):
        marker = self.sms_fac_1.getMarker()
        expected_marker = "['facility1',2,'street','village','commune','district','province','phone; phone-1st; phone_2'," +\
            "'hours','fp-service','safe-abortion','safe-abortion-12','id13','prov-khmer','dist-khmer','com-khmer'," +\
            "'village-khmer','street-khmer','name-khmer']"
        self.assertEqual(marker, unicode(expected_marker))

    def test_facilities_marker(self):
        return_value = Mock()
        def extra(*args, **kwargs):
            return [self.sms_fac_1, self.sms_fac_2, self.sms_fac_3]
        return_value.extra = extra

        with patch("referral_system.models.SmsFac.objects.all") as sms_facs_mock:
            sms_facs_mock.return_value = return_value
            from referral_system.classes.Referral import Referral
            referral = Referral()
            referral.getFacilityMarkerList()
            self.maxDiff = None
            expected = "%s,%s" % (self.sms_fac_1.getMarker(), self.sms_fac_3.getMarker())
            self.assertEqual(referral.facilityMarkerList, expected)


        
    