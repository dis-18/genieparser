# Python
import unittest
from unittest.mock import Mock

# ATS
from ats.topology import Device
from ats.topology import loader

# Metaparser
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# BigIP get_ltm_monitorradius
from genie.libs.parser.bigip.get_ltm_monitorradius import LtmMonitorRadius

# ==================================
# Unit test for parsing BigIP URL '/mgmt/tm/ltm/monitor/radius'
# ==================================


class FakeResponse(object):
    def json(self):
        return {
            "kind": "tm:ltm:monitor:radius:radiuscollectionstate",
            "selfLink": "https://localhost/mgmt/tm/ltm/monitor/radius?ver=14.1.2.1",
            "items": [
                {
                    "kind": "tm:ltm:monitor:radius:radiusstate",
                    "name": "radius",
                    "partition": "Common",
                    "fullPath": "/Common/radius",
                    "generation": 0,
                    "selfLink": "https://localhost/mgmt/tm/ltm/monitor/radius/~Common~radius?ver=14.1.2.1",
                    "debug": "no",
                    "destination": "*:*",
                    "interval": 10,
                    "manualResume": "disabled",
                    "timeUntilUp": 0,
                    "timeout": 31,
                    "upInterval": 0,
                }
            ],
        }


class test_get_ltm_monitorradius(unittest.TestCase):

    maxDiff = None

    empty_output = {"get.return_value": {}}

    golden_parsed_output = {
        "items": [
            {
                "debug": "no",
                "destination": "*:*",
                "fullPath": "/Common/radius",
                "generation": 0,
                "interval": 10,
                "kind": "tm:ltm:monitor:radius:radiusstate",
                "manualResume": "disabled",
                "name": "radius",
                "partition": "Common",
                "selfLink": "https://localhost/mgmt/tm/ltm/monitor/radius/~Common~radius?ver=14.1.2.1",
                "timeUntilUp": 0,
                "timeout": 31,
                "upInterval": 0,
            }
        ],
        "kind": "tm:ltm:monitor:radius:radiuscollectionstate",
        "selfLink": "https://localhost/mgmt/tm/ltm/monitor/radius?ver=14.1.2.1",
    }

    golden_output = {"get.return_value": FakeResponse()}

    # def test_empty(self):
    #     self.device1 = Mock(**self.empty_output)
    #     obj = LtmMonitorRadius(device=self.device1, alias='rest', via='rest', context='rest')
    #     with self.assertRaises(SchemaEmptyParserError):
    #         parsed_output = obj.parse()

    def test_golden(self):
        self.device = Mock(**self.golden_output)
        obj = LtmMonitorRadius(
            device=self.device, alias="rest", via="rest", context="rest"
        )
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output)


if __name__ == "__main__":
    unittest.main()
