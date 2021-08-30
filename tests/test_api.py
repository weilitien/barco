
import requests


header = {'user-agent': 'Mozilla/5.0'}
endpoint = "https://www.barco.com/services/website/en/WarrantyLister/GetWarrantyResult"


class TestValidNumber:

    def _handle_query_string(self, serial_num, categories=None):
        out_query_string = f"serialNumber={serial_num}&categories=%7B6282E2AA-42D2-4682-8645-581196AE490B%7D%7C%7B18EEDAF9-2AED-4EDF-8941-720587910CBB%7D"
        if categories:
            out_query_string = f"serialNumber={serial_num}&categories={categories}"
        return out_query_string

    def _self_check(self, result_payload):
        expect_index = ["canShowInfo", "deliveryDate", "description", "imageUrl", "installationDate", "partNumber",
                        "serviceDate", "warrantyEndDate"]
        assert result_payload["notFoundMessage"] == ""
        assert result_payload["success"]
        for i in range(0, len(result_payload["results"])):
            for x in result_payload["results"][i]:
                assert x in expect_index

    # TODO: Need to confirm how many categories apply for,
    #  and it might be a defect here, usually POST method returns 201 if it is working.
    def test_valid_serial_number(self):
        test_data = self._handle_query_string("1862337755")
        response = requests.post(endpoint, params=test_data, headers=header)
        response_body = response.json()
        assert response.status_code == 200
        self._self_check(response_body)

    def test_invalid_serial_number(self):
        test_data = self._handle_query_string("12345678")
        response = requests.post(endpoint, params=test_data, headers=header)
        response_body = response.json()
        assert response.status_code == 200
        assert response_body["results"] is None
        assert not response_body["success"]
        assert "We couldn't find a product with this serial number. Please double-check the serial number and try again." in response_body["notFoundMessage"]

    # I think it is a bug, the response content should be aligned with invalid number. And it looks like the description is not completed.
    def test_continuity_serial_number(self):
        test_data = self._handle_query_string("666666")
        response = requests.post(endpoint, params=test_data, headers=header)
        response_body = response.json()
        assert response.status_code == 200
        assert response_body["results"] is None
        assert not response_body["success"]




