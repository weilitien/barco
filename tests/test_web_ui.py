
import pytest
import string
from random import choice
from test_var.test_element_location import input_serial_number_class, get_info_button_css, \
    field_validation_error_class, serial_result_class, result_des_class
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BACOR_URL = "https://www.barco.com/en/clickshare/support/warranty-info"


class TestNormalInput:

    @pytest.mark.parametrize("serial_number", [
        pytest.param("1862337755", id="valid_1")
    ])
    def test_valid_serial_number(self, lunch_web, serial_number):
        web = lunch_web
        web.get(BACOR_URL)
        input_area = web.find_element_by_class_name(input_serial_number_class)
        input_area.send_keys(serial_number)
        web.find_element_by_css_selector(get_info_button_css).click()
        WebDriverWait(web, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, serial_result_class)))
        result = web.find_elements_by_class_name(result_des_class)
        assert len(result) != 0
        for i in result:
            assert i.is_displayed()


class TestAbnormalInput:

    @pytest.mark.parametrize("serial_number", [
        pytest.param("12345678", id="invalid_1")
    ])
    def test_invalid_serial_number(self, lunch_web, serial_number):
        web = lunch_web
        web.get(BACOR_URL)
        input_area = web.find_element_by_class_name(input_serial_number_class)
        input_area.send_keys(serial_number)
        web.find_element_by_css_selector(get_info_button_css).click()
        WebDriverWait(web, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, serial_result_class)))
        warranty_results = web.find_element_by_class_name(serial_result_class)
        assert f"Warranty results for {serial_number}" in warranty_results.text
        assert "We couldn't find a product with this serial number. Please double-check the serial number and try again." in warranty_results.text

    @pytest.mark.skip(reason="Need to confirm if it is a bug or not.")
    @pytest.mark.parametrize("serial_number", [
        pytest.param("666666", id="continuity with 6 characters")
    ])
    # I think it is a bug, the response content should be aligned with invalid number. And it looks like the description is not completed.
    def test_continuity_serial_number(self, lunch_web, serial_number):
        web = lunch_web
        web.get(BACOR_URL)
        input_area = web.find_element_by_class_name(input_serial_number_class)
        input_area.send_keys(serial_number)
        web.find_element_by_css_selector(get_info_button_css).click()
        WebDriverWait(web, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, serial_result_class)))
        warranty_results = web.find_element_by_class_name(serial_result_class)
        assert f"Warranty results for {serial_number}" in warranty_results.text

    @pytest.mark.parametrize("serial_number", [
        pytest.param("".join(choice(string.ascii_letters) for i in range(1)), id="only 1 character"),
        pytest.param("".join(choice(string.digits) for i in range(5)), id="only 5 characters")
    ])
    def test_within_6_characters(self, lunch_web, serial_number):
        web = lunch_web
        web.get(BACOR_URL)
        input_area = web.find_element_by_class_name(input_serial_number_class)
        input_area.send_keys(serial_number)
        web.find_element_by_css_selector(get_info_button_css).click()
        WebDriverWait(web, 5).until(EC.presence_of_element_located((By.CLASS_NAME, field_validation_error_class)))
        error_msg = web.find_elements_by_class_name(field_validation_error_class)
        result_msg = ""
        for i in error_msg:
            if i.text != "":
                result_msg = i.text
        assert result_msg == "Minimum 6 characters required"

    @pytest.mark.parametrize("serial_number", [
        pytest.param("@@@%%%&&&&", id="symbols"),
        pytest.param("這是中文的測試", id="Chinese"),
        pytest.param("ｃｈａｒａｃｔｅｒ", id="full width character")
    ])
    def test_unusual_characters(self, lunch_web, serial_number):
        web = lunch_web
        web.get(BACOR_URL)
        input_area = web.find_element_by_class_name(input_serial_number_class)
        input_area.send_keys(serial_number)
        web.find_element_by_css_selector(get_info_button_css).click()
        WebDriverWait(web, 5).until(EC.presence_of_element_located((By.CLASS_NAME, field_validation_error_class)))
        error_msg = web.find_elements_by_class_name(field_validation_error_class)
        result_msg = ""
        for i in error_msg:
            if i.text != "":
                result_msg = i.text
        assert result_msg == "Please enter a valid serial number"

    def test_empty_serial_number(self, lunch_web):
        web = lunch_web
        web.get(BACOR_URL)
        input_area = web.find_element_by_class_name(input_serial_number_class)
        input_area.send_keys("")
        web.find_element_by_css_selector(get_info_button_css).click()
        WebDriverWait(web, 5).until(EC.presence_of_element_located((By.CLASS_NAME, field_validation_error_class)))
        error_msg = web.find_elements_by_class_name(field_validation_error_class)
        result_msg = ""
        for i in error_msg:
            if i.text != "":
                result_msg = i.text
        assert result_msg == "Please specify a serial number"



