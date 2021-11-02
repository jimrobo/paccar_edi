from dataclasses import dataclass
from typing import Optional, Any, List, Dict, TypeVar, Type, cast, Callable
import dicttoxml
import re
from xml.dom.minidom import parseString
from xml.sax.saxutils import escape
from lxml import etree
import copy
import json
import pprint

T = TypeVar("T")

def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


@dataclass
class PostProcess:
    file_name: Optional[str] = None
    output_folder: Optional[str] = None

    def to_dict(self) -> dict:
        result: dict = {}
        result["FileName"] = from_union([from_str, from_none], self.file_name)
        result["OutputFolder"] = from_union([from_str, from_none], self.output_folder)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class ISLEDIContext:
    interface: Optional[str] = None
    post_process: Optional[str] = None

    def __post_init__(self):
        self.post_process = "MultiShed-xml"

    def to_dict(self) -> dict:
        result: dict = {}
        result["Interface"] = from_union([from_str, from_none], self.interface)
        result["PostProcess"] = from_union([from_str, from_none], self.post_process)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class DocAdd:
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    address_3: Optional[str] = None
    address_code: Optional[str] = None
    address_type: Optional[str] = None
    contact_name: Optional[str] = None
    country_code: Optional[str] = None
    county: Optional[str] = None
    email: Optional[str] = None
    fax: Optional[str] = None
    grp_id: Optional[str] = None
    job_id: Optional[str] = None
    keyname: Optional[str] = None
    line_no: Optional[str] = None
    name: Optional[str] = None
    postcode: Optional[str] = None
    rec_id: Optional[str] = None
    record_link: Optional[str] = None
    reference: Optional[str] = None
    telephone: Optional[str] = None
    telex: Optional[str] = None
    town: Optional[str] = None

    def to_dict(self) -> dict:
        result: dict = {}
        result["address-1"] = from_union([from_str, from_none], self.address_1)
        result["address-2"] = from_union([from_str, from_none], self.address_2)
        result["address-3"] = from_union([from_str, from_none], self.address_3)
        result["address-code"] = from_union([from_str, from_none], self.address_code)
        result["address-type"] = from_union([from_str, from_none], self.address_type)
        result["contact-name"] = from_union([from_str, from_none], self.contact_name)
        result["country-code"] = from_union([from_str, from_none], self.country_code)
        result["county"] = from_union([from_str, from_none], self.county)
        result["email"] = from_union([from_str, from_none], self.email)
        result["fax"] = from_union([from_str, from_none], self.fax)
        result["grp-id"] = from_union([from_str, from_none], self.grp_id)
        result["job-id"] = from_union([from_str, from_none], self.job_id)
        result["keyname"] = from_union([from_str, from_none], self.keyname)
        result["line-no"] = from_union([from_str, from_none], self.line_no)
        result["name"] = from_union([from_str, from_none], self.name)
        result["postcode"] = from_union([from_str, from_none], self.postcode)
        result["rec-id"] = from_union([from_str, from_none], self.rec_id)
        result["record-link"] = from_union([from_str, from_none], self.record_link)
        result["reference"] = from_union([from_str, from_none], self.reference)
        result["telephone"] = from_union([from_str, from_none], self.telephone)
        result["telex"] = from_union([from_str, from_none], self.telex)
        result["town"] = from_union([from_str, from_none], self.town)
        return {k: v for k, v in result.items() if v is not None}

@dataclass
class RecChg:
    all_in: Optional[str] = None
    base_inv_exchange: Optional[str] = None
    base_sales_value: Optional[str] = None
    base_vat_value: Optional[str] = None
    calc_code: Optional[str] = None
    charge_currency: Optional[str] = None
    charge_entry: Optional[str] = None
    charge_order: Optional[str] = None
    charge_rate: Optional[str] = None
    charge_type: Optional[str] = None
    charge_value: Optional[str] = None
    chg_base_exchange: Optional[str] = None
    chg_source: Optional[str] = None
    costcentre: Optional[str] = None
    date_created: Optional[str] = None
    description: Optional[str] = None
    euro_exchange: Optional[str] = None
    euro_value: Optional[str] = None
    euro_vat: Optional[str] = None
    expensecode: Optional[str] = None
    haulage_line: Optional[str] = None
    invoice_currency: Optional[str] = None
    invoicee: Optional[str] = None
    invoice_number: Optional[str] = None
    invoice_value: Optional[str] = None
    invoice_vat: Optional[str] = None
    inv_period: Optional[str] = None
    inv_yearno: Optional[str] = None
    line_no: Optional[str] = None
    maximum_value: Optional[str] = None
    minimum_value: Optional[str] = None
    notes: Optional[str] = None
    orig_id: Optional[str] = None
    orig_line: Optional[str] = None
    orig_link: Optional[str] = None
    prepaid_collect: Optional[str] = None
    rec_id: Optional[str] = None
    rec_no: Optional[str] = None
    record_link: Optional[str] = None
    scs_processed: Optional[str] = None
    trans_date: Optional[str] = None
    vat_code: Optional[str] = None
    vat_exchange: Optional[str] = None
    vat_rate: Optional[str] = None

    def to_dict(self) -> dict:
        result: dict = {}
        result["all-in"] = from_union([from_str, from_none], self.all_in)
        result["base-inv-exchange"] = from_union([from_str, from_none], self.base_inv_exchange)
        result["base-sales-value"] = from_union([from_str, from_none], self.base_sales_value)
        result["base-vat-value"] = from_union([from_str, from_none], self.base_vat_value)
        result["calc-code"] = from_union([from_str, from_none], self.calc_code)
        result["charge-currency"] = from_union([from_str, from_none], self.charge_currency)
        result["charge-entry"] = from_union([from_str, from_none], self.charge_entry)
        result["charge-order"] = from_union([from_str, from_none], self.charge_order)
        result["charge-rate"] = from_union([from_str, from_none], self.charge_rate)
        result["charge-type"] = from_union([from_str, from_none], self.charge_type)
        result["charge-value"] = from_union([from_str, from_none], self.charge_value)
        result["chg-base-exchange"] = from_union([from_str, from_none], self.chg_base_exchange)
        result["chg-source"] = from_union([from_str, from_none], self.chg_source)
        result["costcentre"] = from_union([from_str, from_none], self.costcentre)
        result["date-created"] = from_union([from_str, from_none], self.date_created)
        result["description"] = from_union([from_str, from_none], self.description)
        result["euro-exchange"] = from_union([from_str, from_none], self.euro_exchange)
        result["euro-value"] = from_union([from_str, from_none], self.euro_value)
        result["euro-vat"] = from_union([from_str, from_none], self.euro_vat)
        result["expensecode"] = from_union([from_str, from_none], self.expensecode)
        result["haulageLine"] = from_union([from_str, from_none], self.haulage_line)
        result["invoice-currency"] = from_union([from_str, from_none], self.invoice_currency)
        result["invoicee"] = from_union([from_str, from_none], self.invoicee)
        result["invoice-number"] = from_union([from_str, from_none], self.invoice_number)
        result["invoice-value"] = from_union([from_str, from_none], self.invoice_value)
        result["invoice-vat"] = from_union([from_str, from_none], self.invoice_vat)
        result["inv-period"] = from_union([from_str, from_none], self.inv_period)
        result["inv-yearno"] = from_union([from_str, from_none], self.inv_yearno)
        result["line-no"] = from_union([from_str, from_none], self.line_no)
        result["maximum-value"] = from_union([from_str, from_none], self.maximum_value)
        result["minimum-value"] = from_union([from_str, from_none], self.minimum_value)
        result["notes"] = from_union([from_str, from_none], self.notes)
        result["orig-id"] = from_union([from_str, from_none], self.orig_id)
        result["orig-line"] = from_union([from_str, from_none], self.orig_line)
        result["orig-link"] = from_union([from_str, from_none], self.orig_link)
        result["prepaid-collect"] = from_union([from_str, from_none], self.prepaid_collect)
        result["rec-id"] = from_union([from_str, from_none], self.rec_id)
        result["rec-no"] = from_union([from_str, from_none], self.rec_no)
        result["record-link"] = from_union([from_str, from_none], self.record_link)
        result["scs-processed"] = from_union([from_str, from_none], self.scs_processed)
        result["trans-date"] = from_union([from_str, from_none], self.trans_date)
        result["vat-code"] = from_union([from_str, from_none], self.vat_code)
        result["vat-exchange"] = from_union([from_str, from_none], self.vat_exchange)
        result["vat-rate"] = from_union([from_str, from_none], self.vat_rate)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class RecJny:
    airline_prefix: Optional[str] = None
    arr_date_1: Optional[str] = None
    arr_date_2: Optional[str] = None
    arr_date_3: Optional[str] = None
    arr_date_4: Optional[str] = None
    arr_date_5: Optional[str] = None
    arr_date_6: Optional[str] = None
    arr_time_1: Optional[str] = None
    arr_time_2: Optional[str] = None
    arr_time_3: Optional[str] = None
    arr_time_4: Optional[str] = None
    arr_time_5: Optional[str] = None
    arr_time_6: Optional[str] = None
    car_code_1: Optional[str] = None
    car_code_2: Optional[str] = None
    car_code_3: Optional[str] = None
    car_code_4: Optional[str] = None
    car_code_5: Optional[str] = None
    car_code_6: Optional[str] = None
    car_desc_1: Optional[str] = None
    car_desc_2: Optional[str] = None
    car_desc_3: Optional[str] = None
    car_desc_4: Optional[str] = None
    car_desc_5: Optional[str] = None
    car_desc_6: Optional[str] = None
    char_prefix: Optional[str] = None
    date_idx1: Optional[str] = None
    dept_date_1: Optional[str] = None
    dept_date_2: Optional[str] = None
    dept_date_3: Optional[str] = None
    dept_date_4: Optional[str] = None
    dept_date_5: Optional[str] = None
    dept_date_6: Optional[str] = None
    dept_time_1: Optional[str] = None
    dept_time_2: Optional[str] = None
    dept_time_3: Optional[str] = None
    dept_time_4: Optional[str] = None
    dept_time_5: Optional[str] = None
    dept_time_6: Optional[str] = None
    dv_car_curr: Optional[str] = None
    dv_carriage: Optional[str] = None
    dv_cus_curr: Optional[str] = None
    dv_customs: Optional[str] = None
    eda: Optional[str] = None
    eta: Optional[str] = None
    ext_code_1: Optional[str] = None
    ext_code_2: Optional[str] = None
    ext_code_3: Optional[str] = None
    ext_code_4: Optional[str] = None
    ext_code_5: Optional[str] = None
    ext_code_6: Optional[str] = None
    ext_date_1: Optional[str] = None
    ext_date_2: Optional[str] = None
    ext_date_3: Optional[str] = None
    ext_date_4: Optional[str] = None
    ext_date_5: Optional[str] = None
    ext_date_6: Optional[str] = None
    ext_desc_1: Optional[str] = None
    ext_desc_2: Optional[str] = None
    ext_desc_3: Optional[str] = None
    ext_desc_4: Optional[str] = None
    ext_desc_5: Optional[str] = None
    ext_desc_6: Optional[str] = None
    flight_by_1: Optional[str] = None
    flight_by_2: Optional[str] = None
    flight_by_3: Optional[str] = None
    flight_date_1: Optional[str] = None
    flight_date_2: Optional[str] = None
    flight_idx1: Optional[str] = None
    flight_idx2: Optional[str] = None
    flight_idx3: Optional[str] = None
    flight_idx4: Optional[str] = None
    flight_idx5: Optional[str] = None
    flight_no_1: Optional[str] = None
    flight_no_2: Optional[str] = None
    flight_prefix_1: Optional[str] = None
    flight_prefix_2: Optional[str] = None
    flight_time_1: Optional[str] = None
    flight_time_2: Optional[str] = None
    flight_time_3: Optional[str] = None
    flight_to_1: Optional[str] = None
    flight_to_2: Optional[str] = None
    flight_to_3: Optional[str] = None
    insurance: Optional[str] = None
    jny_code_1: Optional[str] = None
    jny_code_2: Optional[str] = None
    jny_code_3: Optional[str] = None
    jny_code_4: Optional[str] = None
    jny_code_5: Optional[str] = None
    jny_code_6: Optional[str] = None
    jny_desc_1: Optional[str] = None
    jny_desc_2: Optional[str] = None
    jny_desc_3: Optional[str] = None
    jny_desc_4: Optional[str] = None
    jny_desc_5: Optional[str] = None
    jny_desc_6: Optional[str] = None
    loc_code_1: Optional[str] = None
    loc_code_2: Optional[str] = None
    loc_code_3: Optional[str] = None
    loc_code_4: Optional[str] = None
    loc_code_5: Optional[str] = None
    loc_code_6: Optional[str] = None
    loc_desc_1: Optional[str] = None
    loc_desc_2: Optional[str] = None
    loc_desc_3: Optional[str] = None
    loc_desc_4: Optional[str] = None
    loc_desc_5: Optional[str] = None
    loc_desc_6: Optional[str] = None
    mawb: Optional[str] = None
    mawb_clerk: Optional[str] = None
    mawb_date: Optional[str] = None
    port_of_discharge: Optional[str] = None
    port_of_loading: Optional[str] = None
    rec_id: Optional[str] = None
    record_link: Optional[str] = None
    third_flight_date: Optional[str] = None
    third_flight_no: Optional[str] = None
    third_flight_prefix: Optional[str] = None
    truck_leg: Optional[str] = None


    def to_dict(self) -> dict:
        result: dict = {}
        result["airline-prefix"] = from_union([from_str, from_none], self.airline_prefix)
        result["arr-date-1"] = from_union([from_str, from_none], self.arr_date_1)
        result["arr-date-2"] = from_union([from_str, from_none], self.arr_date_2)
        result["arr-date-3"] = from_union([from_str, from_none], self.arr_date_3)
        result["arr-date-4"] = from_union([from_str, from_none], self.arr_date_4)
        result["arr-date-5"] = from_union([from_str, from_none], self.arr_date_5)
        result["arr-date-6"] = from_union([from_str, from_none], self.arr_date_6)
        result["arr-time-1"] = from_union([from_str, from_none], self.arr_time_1)
        result["arr-time-2"] = from_union([from_str, from_none], self.arr_time_2)
        result["arr-time-3"] = from_union([from_str, from_none], self.arr_time_3)
        result["arr-time-4"] = from_union([from_str, from_none], self.arr_time_4)
        result["arr-time-5"] = from_union([from_str, from_none], self.arr_time_5)
        result["arr-time-6"] = from_union([from_str, from_none], self.arr_time_6)
        result["car-code-1"] = from_union([from_str, from_none], self.car_code_1)
        result["car-code-2"] = from_union([from_str, from_none], self.car_code_2)
        result["car-code-3"] = from_union([from_str, from_none], self.car_code_3)
        result["car-code-4"] = from_union([from_str, from_none], self.car_code_4)
        result["car-code-5"] = from_union([from_str, from_none], self.car_code_5)
        result["car-code-6"] = from_union([from_str, from_none], self.car_code_6)
        result["car-desc-1"] = from_union([from_str, from_none], self.car_desc_1)
        result["car-desc-2"] = from_union([from_str, from_none], self.car_desc_2)
        result["car-desc-3"] = from_union([from_str, from_none], self.car_desc_3)
        result["car-desc-4"] = from_union([from_str, from_none], self.car_desc_4)
        result["car-desc-5"] = from_union([from_str, from_none], self.car_desc_5)
        result["car-desc-6"] = from_union([from_str, from_none], self.car_desc_6)
        result["char-prefix"] = from_union([from_str, from_none], self.char_prefix)
        result["date-idx1"] = from_union([from_str, from_none], self.date_idx1)
        result["dept-date-1"] = from_union([from_str, from_none], self.dept_date_1)
        result["dept-date-2"] = from_union([from_str, from_none], self.dept_date_2)
        result["dept-date-3"] = from_union([from_str, from_none], self.dept_date_3)
        result["dept-date-4"] = from_union([from_str, from_none], self.dept_date_4)
        result["dept-date-5"] = from_union([from_str, from_none], self.dept_date_5)
        result["dept-date-6"] = from_union([from_str, from_none], self.dept_date_6)
        result["dept-time-1"] = from_union([from_str, from_none], self.dept_time_1)
        result["dept-time-2"] = from_union([from_str, from_none], self.dept_time_2)
        result["dept-time-3"] = from_union([from_str, from_none], self.dept_time_3)
        result["dept-time-4"] = from_union([from_str, from_none], self.dept_time_4)
        result["dept-time-5"] = from_union([from_str, from_none], self.dept_time_5)
        result["dept-time-6"] = from_union([from_str, from_none], self.dept_time_6)
        result["dv-car-curr"] = from_union([from_str, from_none], self.dv_car_curr)
        result["dv-carriage"] = from_union([from_str, from_none], self.dv_carriage)
        result["dv-cus-curr"] = from_union([from_str, from_none], self.dv_cus_curr)
        result["dv-customs"] = from_union([from_str, from_none], self.dv_customs)
        result["eda"] = from_union([from_str, from_none], self.eda)
        result["eta"] = from_union([from_str, from_none], self.eta)
        result["ext-code-1"] = from_union([from_str, from_none], self.ext_code_1)
        result["ext-code-2"] = from_union([from_str, from_none], self.ext_code_2)
        result["ext-code-3"] = from_union([from_str, from_none], self.ext_code_3)
        result["ext-code-4"] = from_union([from_str, from_none], self.ext_code_4)
        result["ext-code-5"] = from_union([from_str, from_none], self.ext_code_5)
        result["ext-code-6"] = from_union([from_str, from_none], self.ext_code_6)
        result["ext-date-1"] = from_union([from_str, from_none], self.ext_date_1)
        result["ext-date-2"] = from_union([from_str, from_none], self.ext_date_2)
        result["ext-date-3"] = from_union([from_str, from_none], self.ext_date_3)
        result["ext-date-4"] = from_union([from_str, from_none], self.ext_date_4)
        result["ext-date-5"] = from_union([from_str, from_none], self.ext_date_5)
        result["ext-date-6"] = from_union([from_str, from_none], self.ext_date_6)
        result["ext-desc-1"] = from_union([from_str, from_none], self.ext_desc_1)
        result["ext-desc-2"] = from_union([from_str, from_none], self.ext_desc_2)
        result["ext-desc-3"] = from_union([from_str, from_none], self.ext_desc_3)
        result["ext-desc-4"] = from_union([from_str, from_none], self.ext_desc_4)
        result["ext-desc-5"] = from_union([from_str, from_none], self.ext_desc_5)
        result["ext-desc-6"] = from_union([from_str, from_none], self.ext_desc_6)
        result["flight-by-1"] = from_union([from_str, from_none], self.flight_by_1)
        result["flight-by-2"] = from_union([from_str, from_none], self.flight_by_2)
        result["flight-by-3"] = from_union([from_str, from_none], self.flight_by_3)
        result["flight-date-1"] = from_union([from_str, from_none], self.flight_date_1)
        result["flight-date-2"] = from_union([from_str, from_none], self.flight_date_2)
        result["flight-idx1"] = from_union([from_str, from_none], self.flight_idx1)
        result["flight-idx2"] = from_union([from_str, from_none], self.flight_idx2)
        result["flight-idx3"] = from_union([from_str, from_none], self.flight_idx3)
        result["flight-idx4"] = from_union([from_str, from_none], self.flight_idx4)
        result["flight-idx5"] = from_union([from_str, from_none], self.flight_idx5)
        result["flight-no-1"] = from_union([from_str, from_none], self.flight_no_1)
        result["flight-no-2"] = from_union([from_str, from_none], self.flight_no_2)
        result["flight-prefix-1"] = from_union([from_str, from_none], self.flight_prefix_1)
        result["flight-prefix-2"] = from_union([from_str, from_none], self.flight_prefix_2)
        result["flight-time-1"] = from_union([from_str, from_none], self.flight_time_1)
        result["flight-time-2"] = from_union([from_str, from_none], self.flight_time_2)
        result["flight-time-3"] = from_union([from_str, from_none], self.flight_time_3)
        result["flight-to-1"] = from_union([from_str, from_none], self.flight_to_1)
        result["flight-to-2"] = from_union([from_str, from_none], self.flight_to_2)
        result["flight-to-3"] = from_union([from_str, from_none], self.flight_to_3)
        result["insurance"] = from_union([from_str, from_none], self.insurance)
        result["jny-code-1"] = from_union([from_str, from_none], self.jny_code_1)
        result["jny-code-2"] = from_union([from_str, from_none], self.jny_code_2)
        result["jny-code-3"] = from_union([from_str, from_none], self.jny_code_3)
        result["jny-code-4"] = from_union([from_str, from_none], self.jny_code_4)
        result["jny-code-5"] = from_union([from_str, from_none], self.jny_code_5)
        result["jny-code-6"] = from_union([from_str, from_none], self.jny_code_6)
        result["jny-desc-1"] = from_union([from_str, from_none], self.jny_desc_1)
        result["jny-desc-2"] = from_union([from_str, from_none], self.jny_desc_2)
        result["jny-desc-3"] = from_union([from_str, from_none], self.jny_desc_3)
        result["jny-desc-4"] = from_union([from_str, from_none], self.jny_desc_4)
        result["jny-desc-5"] = from_union([from_str, from_none], self.jny_desc_5)
        result["jny-desc-6"] = from_union([from_str, from_none], self.jny_desc_6)
        result["loc-code-1"] = from_union([from_str, from_none], self.loc_code_1)
        result["loc-code-2"] = from_union([from_str, from_none], self.loc_code_2)
        result["loc-code-3"] = from_union([from_str, from_none], self.loc_code_3)
        result["loc-code-4"] = from_union([from_str, from_none], self.loc_code_4)
        result["loc-code-5"] = from_union([from_str, from_none], self.loc_code_5)
        result["loc-code-6"] = from_union([from_str, from_none], self.loc_code_6)
        result["loc-desc-1"] = from_union([from_str, from_none], self.loc_desc_1)
        result["loc-desc-2"] = from_union([from_str, from_none], self.loc_desc_2)
        result["loc-desc-3"] = from_union([from_str, from_none], self.loc_desc_3)
        result["loc-desc-4"] = from_union([from_str, from_none], self.loc_desc_4)
        result["loc-desc-5"] = from_union([from_str, from_none], self.loc_desc_5)
        result["loc-desc-6"] = from_union([from_str, from_none], self.loc_desc_6)
        result["mawb"] = from_union([from_str, from_none], self.mawb)
        result["mawb-clerk"] = from_union([from_str, from_none], self.mawb_clerk)
        result["mawb-date"] = from_union([from_str, from_none], self.mawb_date)
        result["port-of-discharge"] = from_union([from_str, from_none], self.port_of_discharge)
        result["port-of-loading"] = from_union([from_str, from_none], self.port_of_loading)
        result["rec-id"] = from_union([from_str, from_none], self.rec_id)
        result["record-link"] = from_union([from_str, from_none], self.record_link)
        result["third-flight-date"] = from_union([from_str, from_none], self.third_flight_date)
        result["third-flight-no"] = from_union([from_str, from_none], self.third_flight_no)
        result["third-flight-prefix"] = from_union([from_str, from_none], self.third_flight_prefix)
        result["truck-leg"] = from_union([from_str, from_none], self.truck_leg)
        return {k: v for k, v in result.items() if v is not None}



@dataclass
class JobHdr:
    acc_info: Optional[str] = None
    account_manager: Optional[str] = None
    actual_arrival_date: Optional[str] = None
    actual_arrival_time: Optional[str] = None
    actual_cost_total: Optional[str] = None
    actual_dept_date: Optional[str] = None
    actual_dept_time: Optional[str] = None
    address_code: Optional[str] = None
    address_ctry: Optional[str] = None
    address_name: Optional[str] = None
    address_town: Optional[str] = None
    ams_sent: Optional[str] = None
    analysis_code_1: Optional[str] = None
    analysis_code_2: Optional[str] = None
    analysis_code_3: Optional[str] = None
    analysis_code_4: Optional[str] = None
    analysis_descr_1: Optional[str] = None
    analysis_descr_2: Optional[str] = None
    analysis_descr_3: Optional[str] = None
    analysis_descr_4: Optional[str] = None
    analysis_label_1: Optional[str] = None
    analysis_label_2: Optional[str] = None
    analysis_label_3: Optional[str] = None
    analysis_label_4: Optional[str] = None
    analysis_lookup_1: Optional[str] = None
    analysis_lookup_2: Optional[str] = None
    analysis_lookup_3: Optional[str] = None
    analysis_lookup_4: Optional[str] = None
    arrival_date: Optional[str] = None
    as_agreed: Optional[str] = None
    back_colour: Optional[str] = None
    baf_percentage: Optional[str] = None
    bill_of_lading: Optional[str] = None
    bol_copy: Optional[str] = None
    bol_issuer_code: Optional[str] = None
    bol_orig: Optional[str] = None
    bol_received: Optional[str] = None
    bol_released: Optional[str] = None
    bol_status: Optional[str] = None
    bond_code: Optional[str] = None
    caf_percentage: Optional[str] = None
    cargo_desc: Optional[str] = None
    cargo_docs: Optional[str] = None
    cargo_only: Optional[str] = None
    carrier: Optional[str] = None
    carrier_bol_copy: Optional[str] = None
    carrier_bol_orig: Optional[str] = None
    carrier_code: Optional[str] = None
    carrier_ctry: Optional[str] = None
    carrier_name: Optional[str] = None
    carrier_town: Optional[str] = None
    chg_weight: Optional[str] = None
    chg_weight_2: Optional[str] = None
    clearance_date: Optional[str] = None
    clearance_route: Optional[str] = None
    clearance_time: Optional[str] = None
    clear_code: Optional[str] = None
    clear_ctry: Optional[str] = None
    clear_name: Optional[str] = None
    clear_town: Optional[str] = None
    close_out_date: Optional[str] = None
    close_out_time: Optional[str] = None
    cnt_id: Optional[str] = None
    cod: Optional[str] = None
    cod_amount: Optional[str] = None
    cod_currency: Optional[str] = None
    col_date: Optional[str] = None
    col_del: Optional[str] = None
    col_time: Optional[str] = None
    col_town: Optional[str] = None
    company: Optional[str] = None
    consignee_code: Optional[str] = None
    consignee_ctry: Optional[str] = None
    consignee_name: Optional[str] = None
    consignee_town: Optional[str] = None
    consignor_code: Optional[str] = None
    consignor_ctry: Optional[str] = None
    consignor_name: Optional[str] = None
    consignor_town: Optional[str] = None
    contact_email: Optional[str] = None
    contact_name: Optional[str] = None
    contact_tel: Optional[str] = None
    container_number: Optional[str] = None
    container_seal: Optional[str] = None
    cont_count_1: Optional[str] = None
    cont_count_2: Optional[str] = None
    cont_count_3: Optional[str] = None
    cont_count_4: Optional[str] = None
    cont_count_5: Optional[str] = None
    cont_count_6: Optional[str] = None
    cont_count_7: Optional[str] = None
    cont_count_8: Optional[str] = None
    cont_count_9: Optional[str] = None
    cont_count_10: Optional[str] = None
    cont_size_1: Optional[str] = None
    cont_size_2: Optional[str] = None
    cont_size_3: Optional[str] = None
    cont_size_4: Optional[str] = None
    cont_size_5: Optional[str] = None
    cont_size_6: Optional[str] = None
    cont_size_7: Optional[str] = None
    cont_size_8: Optional[str] = None
    cont_size_9: Optional[str] = None
    cont_size_10: Optional[str] = None
    cont_summary: Optional[str] = None
    country_code: Optional[str] = None
    courier_awb: Optional[str] = None
    courier_awb_date: Optional[str] = None
    credit_card_expiry: Optional[str] = None
    credit_card_issue: Optional[str] = None
    credit_card_no: Optional[str] = None
    cube: Optional[str] = None
    cube_type: Optional[str] = None
    curuser: Optional[str] = None
    custom_status: Optional[str] = None
    cust_ref: Optional[str] = None
    cust_ref2: Optional[str] = None
    cw_divisor: Optional[str] = None
    decln_part_no: Optional[str] = None
    deferment_number: Optional[str] = None
    del_date: Optional[str] = None
    del_disp: Optional[str] = None
    delivered_date: Optional[str] = None
    delivered_time: Optional[str] = None
    del_time: Optional[str] = None
    del_town: Optional[str] = None
    depot: Optional[str] = None
    dep_status: Optional[str] = None
    dest_instruction: Optional[str] = None
    display_status: Optional[str] = None
    display_status_date: Optional[str] = None
    driver: Optional[str] = None
    driver_mobile: Optional[str] = None
    duty_applicable: Optional[str] = None
    duty_goods_total: Optional[str] = None
    duty_grand_total: Optional[str] = None
    duty_invoicee: Optional[str] = None
    duty_value: Optional[str] = None
    duty_vat_total: Optional[str] = None
    edi_status: Optional[str] = None
    entered_cube: Optional[str] = None
    entered_wgt: Optional[str] = None
    entry_created: Optional[str] = None
    entry_lodged: Optional[str] = None
    entry_number: Optional[str] = None
    equipment: Optional[str] = None
    estimated_arrival_date: Optional[str] = None
    estimated_arrival_time: Optional[str] = None
    estimated_dept_date: Optional[str] = None
    estimated_dept_time: Optional[str] = None
    estimate_matched_total: Optional[str] = None
    estimate_outstanding_total: Optional[str] = None
    estimate_total: Optional[str] = None
    excise_duty_value: Optional[str] = None
    fac_percentage: Optional[str] = None
    final_desc: Optional[str] = None
    final_dest: Optional[str] = None
    flight_type: Optional[str] = None
    fore_colour: Optional[str] = None
    foreign_agent: Optional[str] = None
    foreign_ctry: Optional[str] = None
    foreign_name: Optional[str] = None
    foreign_town: Optional[str] = None
    free_domicile: Optional[str] = None
    freight_payable_at: Optional[str] = None
    from_quote: Optional[str] = None
    frtctrl_ref: Optional[str] = None
    ft_cube: Optional[str] = None
    grn: Optional[str] = None
    grp_disp: Optional[str] = None
    grp_id: Optional[str] = None
    haulage_provider: Optional[str] = None
    haulier_code: Optional[str] = None
    haulier_ctry: Optional[str] = None
    haulier_name: Optional[str] = None
    haulier_town: Optional[str] = None
    hawb: Optional[str] = None
    hawb_char: Optional[str] = None
    hawb_date: Optional[str] = None
    haz_docs: Optional[str] = None
    insured: Optional[str] = None
    inter_job_id: Optional[str] = None
    inter_ship_id: Optional[str] = None
    invoice_currency: Optional[str] = None
    invoicee: Optional[str] = None
    inv_req: Optional[str] = None
    issuing_carrier_text: Optional[str] = None
    job_country_code: Optional[str] = None
    job_date: Optional[str] = None
    job_dept: Optional[str] = None
    job_disp: Optional[str] = None
    job_docs: Optional[str] = None
    job_id: Optional[str] = None
    job_no: Optional[str] = None
    job_office: Optional[str] = None
    job_ok_date: Optional[str] = None
    job_period: Optional[str] = None
    job_process: Optional[str] = None
    job_ready: Optional[str] = None
    job_route: Optional[str] = None
    job_status: Optional[str] = None
    job_time: Optional[str] = None
    job_tracked: Optional[str] = None
    job_year: Optional[str] = None
    kgs_weight: Optional[str] = None
    kgs_weight_nett: Optional[str] = None
    known_shipper: Optional[str] = None
    lbs_chg: Optional[str] = None
    lbs_vol: Optional[str] = None
    lbs_weight_nett: Optional[str] = None
    lbs_wgt: Optional[str] = None
    letter_of_credit: Optional[str] = None
    letter_of_credit_by: Optional[str] = None
    letter_of_credit_date: Optional[str] = None
    letter_of_credit_no: Optional[str] = None
    licence: Optional[str] = None
    loading_meters: Optional[str] = None
    load_type: Optional[str] = None
    local_agent: Optional[str] = None
    local_ctry: Optional[str] = None
    local_name: Optional[str] = None
    local_town: Optional[str] = None
    marks: Optional[str] = None
    mawb_char: Optional[str] = None
    mshed_crn: Optional[str] = None
    ncts_mrn: Optional[str] = None
    ncts_status: Optional[str] = None
    # notify_code_1: Optional[str] = None
    # notify_code_2: Optional[str] = None
    # notify_code_3: Optional[str] = None
    # notify_code_4: Optional[str] = None
    # notify_ctry_1: Optional[str] = None
    # notify_ctry_2: Optional[str] = None
    # notify_ctry_3: Optional[str] = None
    # notify_ctry_4: Optional[str] = None
    # notify_name_1: Optional[str] = None
    # notify_name_2: Optional[str] = None
    # notify_name_3: Optional[str] = None
    # notify_name_4: Optional[str] = None
    # notify_town_1: Optional[str] = None
    # notify_town_2: Optional[str] = None
    # notify_town_3: Optional[str] = None
    # notify_town_4: Optional[str] = None
    num_labels: Optional[str] = None
    ocean_bill: Optional[str] = None
    order_numbers: Optional[str] = None
    orig_comp: Optional[str] = None
    orig_dept: Optional[str] = None
    orig_id: Optional[str] = None
    orig_office: Optional[str] = None
    package_type: Optional[str] = None
    pallets: Optional[str] = None
    pe_crn: Optional[str] = None
    perishable_cargo: Optional[str] = None
    pieces: Optional[str] = None
    place_of_clearance: Optional[str] = None
    place_of_delivery: Optional[str] = None
    pod_description: Optional[str] = None
    pol_description: Optional[str] = None
    port_of_discharge: Optional[str] = None
    port_of_loading: Optional[str] = None
    # product_code: Optional[str] = None
    # product_desc: Optional[str] = None
    # profit: Optional[str] = None
    # profit_margin: Optional[str] = None
    # profit_markup: Optional[str] = None
    # rate_id: Optional[str] = None
    # rcp: Optional[str] = None
    receipt: Optional[str] = None
    receipt_desc: Optional[str] = None
    # released: Optional[str] = None
    # required_date: Optional[str] = None
    # required_time: Optional[str] = None
    # restrict_awb_tab_update: Optional[str] = None
    # routed_by: Optional[str] = None
    # sale_person: Optional[str] = None
    # sales_goods_total: Optional[str] = None
    # sales_grand_total: Optional[str] = None
    # sales_lead_type: Optional[str] = None
    # sales_vat_total: Optional[str] = None
    # sau: Optional[str] = None
    # scs_fill: Optional[str] = None
    # second_carrier: Optional[str] = None
    # second_carrier_code: Optional[str] = None
    # second_carrier_country: Optional[str] = None
    # # second_carrier_name: Optional[str] = None
    # second_carrier_town: Optional[str] = None
    # second_eta: Optional[str] = None
    # second_port_code: Optional[str] = None
    # second_port_desc: Optional[str] = None
    # second_sailing_date: Optional[str] = None
    # second_vessel_code: Optional[str] = None
    # second_vessel_name: Optional[str] = None
    # service_code: Optional[str] = None
    # shipped_on_board: Optional[str] = None
    # shipping_line_ref: Optional[str] = None
    # sph_code: Optional[str] = None
    # split_ref: Optional[str] = None
    # status1_date: Optional[str] = None
    # status1_time: Optional[str] = None
    # status_desc: Optional[str] = None
    # sysuser: Optional[str] = None
    # tax_point_date: Optional[str] = None
    # template_id: Optional[str] = None
    # template_link: Optional[str] = None
    # terms_code: Optional[str] = None
    # terms_code_carrier: Optional[str] = None
    # terms_location: Optional[str] = None
    # third_carrier: Optional[str] = None
    # third_carrier_code: Optional[str] = None
    # third_carrier_country: Optional[str] = None
    # third_carrier_name: Optional[str] = None
    # third_carrier_town: Optional[str] = None
    # third_eta: Optional[str] = None
    # third_port_code: Optional[str] = None
    # third_port_desc: Optional[str] = None
    # third_sailing_date: Optional[str] = None
    # third_vessel_code: Optional[str] = None
    # third_vessel_name: Optional[str] = None
    # total20_ft: Optional[str] = None
    # total30_ft: Optional[str] = None
    # total40_ft: Optional[str] = None
    # total_teu: Optional[str] = None
    # total_trailer: Optional[str] = None
    # trade_area_code: Optional[str] = None
    # trailer_number: Optional[str] = None
    # transport_type: Optional[str] = None
    # u_address: Optional[str] = None
    # ucn: Optional[str] = None
    # ucr: Optional[str] = None
    # vat_invoicee: Optional[str] = None
    # vat_value: Optional[str] = None
    # vehicle_booked_date: Optional[str] = None
    # vehicle_reg: Optional[str] = None
    # version_amended: Optional[str] = None
    # version_created: Optional[str] = None
    # vessel_code: Optional[str] = None
    # vessel_name: Optional[str] = None
    # vol_weight: Optional[str] = None
    # voyage_number: Optional[str] = None
    # # wgt_type: Optional[str] = None
    # # whole_code: Optional[str] = None
    # # whole_ctry: Optional[str] = None
    # # whole_name: Optional[str] = None
    # # whole_town: Optional[str] = None
    # # whs_in_date: Optional[str] = None
    # # whs_in_pieces: Optional[str] = None
    # # # whs_out_date: Optional[str] = None
    # # # whs_out_pieces: Optional[str] = None
    # # # whs_reference: Optional[str] = None
    # # # year_period: Optional[str] = None
    # # # zone: Optional[str] = None
    

    def to_dict(self) -> dict:
        result: dict = {}
        result["acc-info"] = from_union([from_str, from_none], self.acc_info)
        result["AccountManager"] = from_union([from_str, from_none], self.account_manager)
        result["actual-arrival-date"] = from_union([from_str, from_none], self.actual_arrival_date)
        result["actual-arrival-time"] = from_union([from_str, from_none], self.actual_arrival_time)
        result["actualCostTotal"] = from_union([from_str, from_none], self.actual_cost_total)
        result["actual-dept-date"] = from_union([from_str, from_none], self.actual_dept_date)
        result["actual-dept-time"] = from_union([from_str, from_none], self.actual_dept_time)
        result["address-code"] = from_union([from_str, from_none], self.address_code)
        result["address-ctry"] = from_union([from_str, from_none], self.address_ctry)
        result["address-name"] = from_union([from_str, from_none], self.address_name)
        result["address-town"] = from_union([from_str, from_none], self.address_town)
        result["ams-sent"] = from_union([from_str, from_none], self.ams_sent)
        result["analysis-code-1"] = from_union([from_str, from_none], self.analysis_code_1)
        result["analysis-code-2"] = from_union([from_str, from_none], self.analysis_code_2)
        result["analysis-code-3"] = from_union([from_str, from_none], self.analysis_code_3)
        result["analysis-code-4"] = from_union([from_str, from_none], self.analysis_code_4)
        result["analysis-descr-1"] = from_union([from_str, from_none], self.analysis_descr_1)
        result["analysis-descr-2"] = from_union([from_str, from_none], self.analysis_descr_2)
        result["analysis-descr-3"] = from_union([from_str, from_none], self.analysis_descr_3)
        result["analysis-descr-4"] = from_union([from_str, from_none], self.analysis_descr_4)
        result["analysis-label-1"] = from_union([from_str, from_none], self.analysis_label_1)
        result["analysis-label-2"] = from_union([from_str, from_none], self.analysis_label_2)
        result["analysis-label-3"] = from_union([from_str, from_none], self.analysis_label_3)
        result["analysis-label-4"] = from_union([from_str, from_none], self.analysis_label_4)
        result["analysis-lookup-1"] = from_union([from_str, from_none], self.analysis_lookup_1)
        result["analysis-lookup-2"] = from_union([from_str, from_none], self.analysis_lookup_2)
        result["analysis-lookup-3"] = from_union([from_str, from_none], self.analysis_lookup_3)
        result["analysis-lookup-4"] = from_union([from_str, from_none], self.analysis_lookup_4)
        result["arrival-date"] = from_union([from_str, from_none], self.arrival_date)
        result["as-agreed"] = from_union([from_str, from_none], self.as_agreed)
        result["back-colour"] = from_union([from_str, from_none], self.back_colour)
        result["baf-percentage"] = from_union([from_str, from_none], self.baf_percentage)
        result["bill-of-lading"] = from_union([from_str, from_none], self.bill_of_lading)
        result["bol-copy"] = from_union([from_str, from_none], self.bol_copy)
        result["bol-issuer-code"] = from_union([from_str, from_none], self.bol_issuer_code)
        result["bol-orig"] = from_union([from_str, from_none], self.bol_orig)
        result["bol-received"] = from_union([from_str, from_none], self.bol_received)
        result["bol-released"] = from_union([from_str, from_none], self.bol_released)
        result["bol-status"] = from_union([from_str, from_none], self.bol_status)
        result["bond-code"] = from_union([from_str, from_none], self.bond_code)
        result["caf-percentage"] = from_union([from_str, from_none], self.caf_percentage)
        result["cargo-desc"] = from_union([from_str, from_none], self.cargo_desc)
        result["cargo-docs"] = from_union([from_str, from_none], self.cargo_docs)
        result["cargo-only"] = from_union([from_str, from_none], self.cargo_only)
        result["carrier"] = from_union([from_str, from_none], self.carrier)
        result["carrier-bol-copy"] = from_union([from_str, from_none], self.carrier_bol_copy)
        result["carrier-bol-orig"] = from_union([from_str, from_none], self.carrier_bol_orig)
        result["carrier-code"] = from_union([from_str, from_none], self.carrier_code)
        result["carrier-ctry"] = from_union([from_str, from_none], self.carrier_ctry)
        result["carrier-name"] = from_union([from_str, from_none], self.carrier_name)
        result["carrier-town"] = from_union([from_str, from_none], self.carrier_town)
        result["chg-weight"] = from_union([from_str, from_none], self.chg_weight)
        result["chg-weight-2"] = from_union([from_str, from_none], self.chg_weight_2)
        result["clearance-date"] = from_union([from_str, from_none], self.clearance_date)
        result["clearance-route"] = from_union([from_str, from_none], self.clearance_route)
        result["clearance-time"] = from_union([from_str, from_none], self.clearance_time)
        result["clear-code"] = from_union([from_str, from_none], self.clear_code)
        result["clear-ctry"] = from_union([from_str, from_none], self.clear_ctry)
        result["clear-name"] = from_union([from_str, from_none], self.clear_name)
        result["clear-town"] = from_union([from_str, from_none], self.clear_town)
        result["close-out-date"] = from_union([from_str, from_none], self.close_out_date)
        result["close-out-time"] = from_union([from_str, from_none], self.close_out_time)
        result["cnt-id"] = from_union([from_str, from_none], self.cnt_id)
        result["cod"] = from_union([from_str, from_none], self.cod)
        result["cod-amount"] = from_union([from_str, from_none], self.cod_amount)
        result["cod-currency"] = from_union([from_str, from_none], self.cod_currency)
        result["col-date"] = from_union([from_str, from_none], self.col_date)
        result["col-del"] = from_union([from_str, from_none], self.col_del)
        result["col-time"] = from_union([from_str, from_none], self.col_time)
        result["col-town"] = from_union([from_str, from_none], self.col_town)
        result["company"] = from_union([from_str, from_none], self.company)
        result["consignee-code"] = from_union([from_str, from_none], self.consignee_code)
        result["consignee-ctry"] = from_union([from_str, from_none], self.consignee_ctry)
        result["consignee-name"] = from_union([from_str, from_none], self.consignee_name)
        result["consignee-town"] = from_union([from_str, from_none], self.consignee_town)
        result["consignor-code"] = from_union([from_str, from_none], self.consignor_code)
        result["consignor-ctry"] = from_union([from_str, from_none], self.consignor_ctry)
        result["consignor-name"] = from_union([from_str, from_none], self.consignor_name)
        result["consignor-town"] = from_union([from_str, from_none], self.consignor_town)
        result["contact-email"] = from_union([from_str, from_none], self.contact_email)
        result["contact-name"] = from_union([from_str, from_none], self.contact_name)
        result["contact-tel"] = from_union([from_str, from_none], self.contact_tel)
        result["container-number"] = from_union([from_str, from_none], self.container_number)
        result["container-seal"] = from_union([from_str, from_none], self.container_seal)
        result["cont-count-1"] = from_union([from_str, from_none], self.cont_count_1)
        result["cont-count-2"] = from_union([from_str, from_none], self.cont_count_2)
        result["cont-count-3"] = from_union([from_str, from_none], self.cont_count_3)
        result["cont-count-4"] = from_union([from_str, from_none], self.cont_count_4)
        result["cont-count-5"] = from_union([from_str, from_none], self.cont_count_5)
        result["cont-count-6"] = from_union([from_str, from_none], self.cont_count_6)
        result["cont-count-7"] = from_union([from_str, from_none], self.cont_count_7)
        result["cont-count-8"] = from_union([from_str, from_none], self.cont_count_8)
        result["cont-count-9"] = from_union([from_str, from_none], self.cont_count_9)
        result["cont-count-10"] = from_union([from_str, from_none], self.cont_count_10)
        result["cont-size-1"] = from_union([from_str, from_none], self.cont_size_1)
        result["cont-size-2"] = from_union([from_str, from_none], self.cont_size_2)
        result["cont-size-3"] = from_union([from_str, from_none], self.cont_size_3)
        result["cont-size-4"] = from_union([from_str, from_none], self.cont_size_4)
        result["cont-size-5"] = from_union([from_str, from_none], self.cont_size_5)
        result["cont-size-6"] = from_union([from_str, from_none], self.cont_size_6)
        result["cont-size-7"] = from_union([from_str, from_none], self.cont_size_7)
        result["cont-size-8"] = from_union([from_str, from_none], self.cont_size_8)
        result["cont-size-9"] = from_union([from_str, from_none], self.cont_size_9)
        result["cont-size-10"] = from_union([from_str, from_none], self.cont_size_10)
        result["cont-summary"] = from_union([from_str, from_none], self.cont_summary)
        result["country-code"] = from_union([from_str, from_none], self.country_code)
        result["courier-awb"] = from_union([from_str, from_none], self.courier_awb)
        result["courier-awb-date"] = from_union([from_str, from_none], self.courier_awb_date)
        result["credit-card-expiry"] = from_union([from_str, from_none], self.credit_card_expiry)
        result["credit-card-issue"] = from_union([from_str, from_none], self.credit_card_issue)
        result["credit-card-no"] = from_union([from_str, from_none], self.credit_card_no)
        result["cube"] = from_union([from_str, from_none], self.cube)
        result["cube-type"] = from_union([from_str, from_none], self.cube_type)
        result["curuser"] = from_union([from_str, from_none], self.curuser)
        result["custom-status"] = from_union([from_str, from_none], self.custom_status)
        result["cust-ref"] = from_union([from_str, from_none], self.cust_ref)
        result["cust-ref2"] = from_union([from_str, from_none], self.cust_ref2)
        result["cw-divisor"] = from_union([from_str, from_none], self.cw_divisor)
        result["decln-part-no"] = from_union([from_str, from_none], self.decln_part_no)
        result["deferment-number"] = from_union([from_str, from_none], self.deferment_number)
        result["del-date"] = from_union([from_str, from_none], self.del_date)
        result["del-disp"] = from_union([from_str, from_none], self.del_disp)
        result["delivered-date"] = from_union([from_str, from_none], self.delivered_date)
        result["delivered-time"] = from_union([from_str, from_none], self.delivered_time)
        result["del-time"] = from_union([from_str, from_none], self.del_time)
        result["del-town"] = from_union([from_str, from_none], self.del_town)
        result["depot"] = from_union([from_str, from_none], self.depot)
        result["dep-status"] = from_union([from_str, from_none], self.dep_status)
        result["dest-instruction"] = from_union([from_str, from_none], self.dest_instruction)
        result["display-status"] = from_union([from_str, from_none], self.display_status)
        result["display-status-date"] = from_union([from_str, from_none], self.display_status_date)
        result["driver"] = from_union([from_str, from_none], self.driver)
        result["driver-mobile"] = from_union([from_str, from_none], self.driver_mobile)
        result["duty-applicable"] = from_union([from_str, from_none], self.duty_applicable)
        result["dutyGoodsTotal"] = from_union([from_str, from_none], self.duty_goods_total)
        result["dutyGrandTotal"] = from_union([from_str, from_none], self.duty_grand_total)
        result["duty-invoicee"] = from_union([from_str, from_none], self.duty_invoicee)
        result["duty-value"] = from_union([from_str, from_none], self.duty_value)
        result["dutyVatTotal"] = from_union([from_str, from_none], self.duty_vat_total)
        result["edi-status"] = from_union([from_str, from_none], self.edi_status)
        result["entered-cube"] = from_union([from_str, from_none], self.entered_cube)
        result["entered-wgt"] = from_union([from_str, from_none], self.entered_wgt)
        result["entry-created"] = from_union([from_str, from_none], self.entry_created)
        result["entry-lodged"] = from_union([from_str, from_none], self.entry_lodged)
        result["entry-number"] = from_union([from_str, from_none], self.entry_number)
        result["equipment"] = from_union([from_str, from_none], self.equipment)
        result["estimated-arrival-date"] = from_union([from_str, from_none], self.estimated_arrival_date)
        result["estimated-arrival-time"] = from_union([from_str, from_none], self.estimated_arrival_time)
        result["estimated-dept-date"] = from_union([from_str, from_none], self.estimated_dept_date)
        result["estimated-dept-time"] = from_union([from_str, from_none], self.estimated_dept_time)
        result["estimateMatchedTotal"] = from_union([from_str, from_none], self.estimate_matched_total)
        result["estimateOutstandingTotal"] = from_union([from_str, from_none], self.estimate_outstanding_total)
        result["estimateTotal"] = from_union([from_str, from_none], self.estimate_total)
        result["excise-duty-value"] = from_union([from_str, from_none], self.excise_duty_value)
        result["fac-percentage"] = from_union([from_str, from_none], self.fac_percentage)
        result["final-desc"] = from_union([from_str, from_none], self.final_desc)
        result["final-dest"] = from_union([from_str, from_none], self.final_dest)
        result["flight-type"] = from_union([from_str, from_none], self.flight_type)
        result["fore-colour"] = from_union([from_str, from_none], self.fore_colour)
        result["foreign-agent"] = from_union([from_str, from_none], self.foreign_agent)
        result["foreign-ctry"] = from_union([from_str, from_none], self.foreign_ctry)
        result["foreign-name"] = from_union([from_str, from_none], self.foreign_name)
        result["foreign-town"] = from_union([from_str, from_none], self.foreign_town)
        result["free-domicile"] = from_union([from_str, from_none], self.free_domicile)
        result["freight-payable-at"] = from_union([from_str, from_none], self.freight_payable_at)
        result["from-quote"] = from_union([from_str, from_none], self.from_quote)
        result["frtctrl-ref"] = from_union([from_str, from_none], self.frtctrl_ref)
        result["ft-cube"] = from_union([from_str, from_none], self.ft_cube)
        result["GRN"] = from_union([from_str, from_none], self.grn)
        result["grp-disp"] = from_union([from_str, from_none], self.grp_disp)
        result["grp-id"] = from_union([from_str, from_none], self.grp_id)
        result["haulage-provider"] = from_union([from_str, from_none], self.haulage_provider)
        result["haulier-code"] = from_union([from_str, from_none], self.haulier_code)
        result["haulier-ctry"] = from_union([from_str, from_none], self.haulier_ctry)
        result["haulier-name"] = from_union([from_str, from_none], self.haulier_name)
        result["haulier-town"] = from_union([from_str, from_none], self.haulier_town)
        result["hawb"] = from_union([from_str, from_none], self.hawb)
        result["hawb-char"] = from_union([from_str, from_none], self.hawb_char)
        result["hawb-date"] = from_union([from_str, from_none], self.hawb_date)
        result["haz-docs"] = from_union([from_str, from_none], self.haz_docs)
        result["insured"] = from_union([from_str, from_none], self.insured)
        result["inter-job-id"] = from_union([from_str, from_none], self.inter_job_id)
        result["inter-ship-id"] = from_union([from_str, from_none], self.inter_ship_id)
        result["invoice-currency"] = from_union([from_str, from_none], self.invoice_currency)
        result["invoicee"] = from_union([from_str, from_none], self.invoicee)
        result["inv-req"] = from_union([from_str, from_none], self.inv_req)
        result["issuing-carrier-text"] = from_union([from_str, from_none], self.issuing_carrier_text)
        result["job-country-code"] = from_union([from_str, from_none], self.job_country_code)
        result["job-date"] = from_union([from_str, from_none], self.job_date)
        result["job-dept"] = from_union([from_str, from_none], self.job_dept)
        result["job-disp"] = from_union([from_str, from_none], self.job_disp)
        result["job-docs"] = from_union([from_str, from_none], self.job_docs)
        result["job-id"] = from_union([from_str, from_none], self.job_id)
        result["job-no"] = from_union([from_str, from_none], self.job_no)
        result["job-office"] = from_union([from_str, from_none], self.job_office)
        result["job-ok-date"] = from_union([from_str, from_none], self.job_ok_date)
        result["job-period"] = from_union([from_str, from_none], self.job_period)
        result["job-process"] = from_union([from_str, from_none], self.job_process)
        result["job-ready"] = from_union([from_str, from_none], self.job_ready)
        result["job-route"] = from_union([from_str, from_none], self.job_route)
        result["job-status"] = from_union([from_str, from_none], self.job_status)
        result["job-time"] = from_union([from_str, from_none], self.job_time)
        result["job-tracked"] = from_union([from_str, from_none], self.job_tracked)
        result["job-year"] = from_union([from_str, from_none], self.job_year)
        result["kgs-weight"] = from_union([from_str, from_none], self.kgs_weight)
        result["kgs-weight-nett"] = from_union([from_str, from_none], self.kgs_weight_nett)
        result["known-shipper"] = from_union([from_str, from_none], self.known_shipper)
        result["lbs-chg"] = from_union([from_str, from_none], self.lbs_chg)
        result["lbs-vol"] = from_union([from_str, from_none], self.lbs_vol)
        result["lbs-weight-nett"] = from_union([from_str, from_none], self.lbs_weight_nett)
        result["lbs-wgt"] = from_union([from_str, from_none], self.lbs_wgt)
        result["letter-of-credit"] = from_union([from_str, from_none], self.letter_of_credit)
        result["letter-of-credit-by"] = from_union([from_str, from_none], self.letter_of_credit_by)
        result["letter-of-credit-date"] = from_union([from_str, from_none], self.letter_of_credit_date)
        result["letter-of-credit-no"] = from_union([from_str, from_none], self.letter_of_credit_no)
        result["licence"] = from_union([from_str, from_none], self.licence)
        result["loading-meters"] = from_union([from_str, from_none], self.loading_meters)
        result["load-type"] = from_union([from_str, from_none], self.load_type)
        result["local-agent"] = from_union([from_str, from_none], self.local_agent)
        result["local-ctry"] = from_union([from_str, from_none], self.local_ctry)
        result["local-name"] = from_union([from_str, from_none], self.local_name)
        result["local-town"] = from_union([from_str, from_none], self.local_town)
        result["marks"] = from_union([from_str, from_none], self.marks)
        result["mawb-char"] = from_union([from_str, from_none], self.mawb_char)
        result["mshed-crn"] = from_union([from_str, from_none], self.mshed_crn)
        result["ncts-mrn"] = from_union([from_str, from_none], self.ncts_mrn)
        result["ncts-status"] = from_union([from_str, from_none], self.ncts_status)
        # result["notify-code-1"] = from_union([from_str, from_none], self.notify_code_1)
        # result["notify-code-2"] = from_union([from_str, from_none], self.notify_code_2)
        # result["notify-code-3"] = from_union([from_str, from_none], self.notify_code_3)
        # result["notify-code-4"] = from_union([from_str, from_none], self.notify_code_4)
        # result["notify-ctry-1"] = from_union([from_str, from_none], self.notify_ctry_1)
        # result["notify-ctry-2"] = from_union([from_str, from_none], self.notify_ctry_2)
        # result["notify-ctry-3"] = from_union([from_str, from_none], self.notify_ctry_3)
        # result["notify-ctry-4"] = from_union([from_str, from_none], self.notify_ctry_4)
        # result["notify-name-1"] = from_union([from_str, from_none], self.notify_name_1)
        # result["notify-name-2"] = from_union([from_str, from_none], self.notify_name_2)
        # result["notify-name-3"] = from_union([from_str, from_none], self.notify_name_3)
        # result["notify-name-4"] = from_union([from_str, from_none], self.notify_name_4)
        # result["notify-town-1"] = from_union([from_str, from_none], self.notify_town_1)
        # result["notify-town-2"] = from_union([from_str, from_none], self.notify_town_2)
        # result["notify-town-3"] = from_union([from_str, from_none], self.notify_town_3)
        # result["notify-town-4"] = from_union([from_str, from_none], self.notify_town_4)
        result["num-labels"] = from_union([from_str, from_none], self.num_labels)
        result["ocean-bill"] = from_union([from_str, from_none], self.ocean_bill)
        result["order-numbers"] = from_union([from_str, from_none], self.order_numbers)
        result["orig-comp"] = from_union([from_str, from_none], self.orig_comp)
        result["orig-dept"] = from_union([from_str, from_none], self.orig_dept)
        result["orig-id"] = from_union([from_str, from_none], self.orig_id)
        result["orig-office"] = from_union([from_str, from_none], self.orig_office)
        result["package-type"] = from_union([from_str, from_none], self.package_type)
        result["pallets"] = from_union([from_str, from_none], self.pallets)
        result["pe-crn"] = from_union([from_str, from_none], self.pe_crn)
        result["perishable-cargo"] = from_union([from_str, from_none], self.perishable_cargo)
        result["pieces"] = from_union([from_str, from_none], self.pieces)
        result["place-of-clearance"] = from_union([from_str, from_none], self.place_of_clearance)
        result["place-of-delivery"] = from_union([from_str, from_none], self.place_of_delivery)
        result["pod-description"] = from_union([from_str, from_none], self.pod_description)
        result["pol-description"] = from_union([from_str, from_none], self.pol_description)
        result["port-of-discharge"] = from_union([from_str, from_none], self.port_of_discharge)
        result["port-of-loading"] = from_union([from_str, from_none], self.port_of_loading)
        # result["product-code"] = from_union([from_str, from_none], self.product_code)
        # result["product-desc"] = from_union([from_str, from_none], self.product_desc)
        # result["profit"] = from_union([from_str, from_none], self.profit)
        # result["profitMargin"] = from_union([from_str, from_none], self.profit_margin)
        # result["profitMarkup"] = from_union([from_str, from_none], self.profit_markup)
        # result["rate-id"] = from_union([from_str, from_none], self.rate_id)
        # result["rcp"] = from_union([from_str, from_none], self.rcp)
        result["receipt"] = from_union([from_str, from_none], self.receipt)
        result["receipt-desc"] = from_union([from_str, from_none], self.receipt_desc)
        # result["released"] = from_union([from_str, from_none], self.released)
        # result["required-date"] = from_union([from_str, from_none], self.required_date)
        # result["required-time"] = from_union([from_str, from_none], self.required_time)
        # result["restrict-awb-tab-update"] = from_union([from_str, from_none], self.restrict_awb_tab_update)
        # result["routed-by"] = from_union([from_str, from_none], self.routed_by)
        # result["sale-person"] = from_union([from_str, from_none], self.sale_person)
        # result["salesGoodsTotal"] = from_union([from_str, from_none], self.sales_goods_total)
        # result["salesGrandTotal"] = from_union([from_str, from_none], self.sales_grand_total)
        # result["sales-lead-type"] = from_union([from_str, from_none], self.sales_lead_type)
        # result["salesVatTotal"] = from_union([from_str, from_none], self.sales_vat_total)
        # result["sau"] = from_union([from_str, from_none], self.sau)
        # result["scs-fill"] = from_union([from_str, from_none], self.scs_fill)
        # result["second-carrier"] = from_union([from_str, from_none], self.second_carrier)
        # result["second-carrier-code"] = from_union([from_str, from_none], self.second_carrier_code)
        # result["second-carrier-country"] = from_union([from_str, from_none], self.second_carrier_country)
        # result["second-carrier-name"] = from_union([from_str, from_none], self.second_carrier_name)
        # result["second-carrier-town"] = from_union([from_str, from_none], self.second_carrier_town)
        # result["second-eta"] = from_union([from_str, from_none], self.second_eta)
        # result["second-port-code"] = from_union([from_str, from_none], self.second_port_code)
        # result["second-port-desc"] = from_union([from_str, from_none], self.second_port_desc)
        # result["second-sailing-date"] = from_union([from_str, from_none], self.second_sailing_date)
        # result["second-vessel-code"] = from_union([from_str, from_none], self.second_vessel_code)
        # result["second-vessel-name"] = from_union([from_str, from_none], self.second_vessel_name)
        # result["service-code"] = from_union([from_str, from_none], self.service_code)
        # result["shipped-on-board"] = from_union([from_str, from_none], self.shipped_on_board)
        # result["shipping-line-ref"] = from_union([from_str, from_none], self.shipping_line_ref)
        # result["sph-code"] = from_union([from_str, from_none], self.sph_code)
        # result["split-ref"] = from_union([from_str, from_none], self.split_ref)
        # result["status1-date"] = from_union([from_str, from_none], self.status1_date)
        # result["status1-time"] = from_union([from_str, from_none], self.status1_time)
        # result["status-desc"] = from_union([from_str, from_none], self.status_desc)
        # result["sysuser"] = from_union([from_str, from_none], self.sysuser)
        # result["tax-point-date"] = from_union([from_str, from_none], self.tax_point_date)
        # result["template-id"] = from_union([from_str, from_none], self.template_id)
        # result["template-link"] = from_union([from_str, from_none], self.template_link)
        # result["terms-code"] = from_union([from_str, from_none], self.terms_code)
        # result["terms-code-carrier"] = from_union([from_str, from_none], self.terms_code_carrier)
        # result["terms-location"] = from_union([from_str, from_none], self.terms_location)
        # result["third-carrier"] = from_union([from_str, from_none], self.third_carrier)
        # result["third-carrier-code"] = from_union([from_str, from_none], self.third_carrier_code)
        # result["third-carrier-country"] = from_union([from_str, from_none], self.third_carrier_country)
        # result["third-carrier-name"] = from_union([from_str, from_none], self.third_carrier_name)
        # result["third-carrier-town"] = from_union([from_str, from_none], self.third_carrier_town)
        # result["third-eta"] = from_union([from_str, from_none], self.third_eta)
        # result["third-port-code"] = from_union([from_str, from_none], self.third_port_code)
        # result["third-port-desc"] = from_union([from_str, from_none], self.third_port_desc)
        # result["third-sailing-date"] = from_union([from_str, from_none], self.third_sailing_date)
        # result["third-vessel-code"] = from_union([from_str, from_none], self.third_vessel_code)
        # result["third-vessel-name"] = from_union([from_str, from_none], self.third_vessel_name)
        # result["total20ft"] = from_union([from_str, from_none], self.total20_ft)
        # result["total30ft"] = from_union([from_str, from_none], self.total30_ft)
        # result["total40ft"] = from_union([from_str, from_none], self.total40_ft)
        # result["totalTEU"] = from_union([from_str, from_none], self.total_teu)
        # result["totalTrailer"] = from_union([from_str, from_none], self.total_trailer)
        # result["trade-area-code"] = from_union([from_str, from_none], self.trade_area_code)
        # result["trailer-number"] = from_union([from_str, from_none], self.trailer_number)
        # result["transport-type"] = from_union([from_str, from_none], self.transport_type)
        # result["u-address"] = from_union([from_str, from_none], self.u_address)
        # result["UCN"] = from_union([from_str, from_none], self.ucn)
        # result["UCR"] = from_union([from_str, from_none], self.ucr)
        # result["vat-invoicee"] = from_union([from_str, from_none], self.vat_invoicee)
        # result["vat-value"] = from_union([from_str, from_none], self.vat_value)
        # result["vehicle-booked-date"] = from_union([from_str, from_none], self.vehicle_booked_date)
        # result["vehicle-reg"] = from_union([from_str, from_none], self.vehicle_reg)
        # result["version-amended"] = from_union([from_str, from_none], self.version_amended)
        # result["version-created"] = from_union([from_str, from_none], self.version_created)
        # result["vessel-code"] = from_union([from_str, from_none], self.vessel_code)
        # result["vessel-name"] = from_union([from_str, from_none], self.vessel_name)
        # result["vol-weight"] = from_union([from_str, from_none], self.vol_weight)
        # result["voyage-number"] = from_union([from_str, from_none], self.voyage_number)
        # result["wgt-type"] = from_union([from_str, from_none], self.wgt_type)
        # result["whole-code"] = from_union([from_str, from_none], self.whole_code)
        # result["whole-ctry"] = from_union([from_str, from_none], self.whole_ctry)
        # result["whole-name"] = from_union([from_str, from_none], self.whole_name)
        # result["whole-town"] = from_union([from_str, from_none], self.whole_town)
        # result["whs-in-date"] = from_union([from_str, from_none], self.whs_in_date)
        # result["whs-in-pieces"] = from_union([from_str, from_none], self.whs_in_pieces)
        # result["whs-out-date"] = from_union([from_str, from_none], self.whs_out_date)
        # result["whs-out-pieces"] = from_union([from_str, from_none], self.whs_out_pieces)
        # result["whs-reference"] = from_union([from_str, from_none], self.whs_reference)
        # result["yearPeriod"] = from_union([from_str, from_none], self.year_period)
        # result["zone"] = from_union([from_str, from_none], self.zone)
        return {k: v for k, v in result.items() if v is not None}

@dataclass
class JobLine:
    awb_add1: Optional[str] = None
    awb_add2: Optional[str] = None
    awb_add3: Optional[str] = None
    bill_of_lading: Optional[str] = None
    call_off_ref: Optional[str] = None
    cargo_currency: Optional[str] = None
    cargo_desc: Optional[str] = None
    cargo_value: Optional[str] = None
    chg_wgt: Optional[str] = None
    commodity_item_no: Optional[str] = None
    consignee: Optional[str] = None
    consignee_ctry: Optional[str] = None
    consignee_name: Optional[str] = None
    consignee_town: Optional[str] = None
    consignor: Optional[str] = None
    consignor_ctry: Optional[str] = None
    consignor_name: Optional[str] = None
    consignor_town: Optional[str] = None
    consolidator: Optional[str] = None
    contact_name: Optional[str] = None
    contacts_ref: Optional[str] = None
    contact_telephone: Optional[str] = None
    courier_payee: Optional[str] = None
    credit_letter_text: Optional[str] = None
    cube: Optional[str] = None
    cube_type: Optional[str] = None
    delivery_date: Optional[str] = None
    entered_cube: Optional[str] = None
    entered_wgt: Optional[str] = None
    failure_comment: Optional[str] = None
    ft_cube: Optional[str] = None
    goods_received: Optional[str] = None
    handling_text: Optional[str] = None
    har_cargo: Optional[str] = None
    haz_contact_fax: Optional[str] = None
    haz_contact_name: Optional[str] = None
    haz_contact_telephone: Optional[str] = None
    haz_ems: Optional[str] = None
    haz_extra_char_1: Optional[str] = None
    haz_extra_char_2: Optional[str] = None
    haz_extra_char_3: Optional[str] = None
    haz_extra_char_4: Optional[str] = None
    haz_extra_char_5: Optional[str] = None
    haz_extra_char_6: Optional[str] = None
    haz_extra_char_7: Optional[str] = None
    haz_extra_char_8: Optional[str] = None
    haz_extra_char_9: Optional[str] = None
    haz_extra_date_1: Optional[str] = None
    haz_extra_date_2: Optional[str] = None
    haz_extra_date_3: Optional[str] = None
    haz_extra_date_4: Optional[str] = None
    haz_extra_date_5: Optional[str] = None
    haz_extra_date_6: Optional[str] = None
    haz_extra_date_7: Optional[str] = None
    haz_extra_date_8: Optional[str] = None
    haz_extra_date_9: Optional[str] = None
    haz_extra_int_1: Optional[str] = None
    haz_extra_int_2: Optional[str] = None
    haz_extra_int_3: Optional[str] = None
    haz_extra_int_4: Optional[str] = None
    haz_extra_int_5: Optional[str] = None
    haz_extra_int_6: Optional[str] = None
    haz_extra_int_7: Optional[str] = None
    haz_extra_int_8: Optional[str] = None
    haz_extra_int_9: Optional[str] = None
    haz_extra_log_1: Optional[str] = None
    haz_extra_log_2: Optional[str] = None
    haz_extra_log_3: Optional[str] = None
    haz_extra_log_4: Optional[str] = None
    haz_extra_log_5: Optional[str] = None
    haz_extra_log_6: Optional[str] = None
    haz_extra_log_7: Optional[str] = None
    haz_extra_log_8: Optional[str] = None
    haz_extra_log_9: Optional[str] = None
    haz_flashpoint: Optional[str] = None
    haz_imco: Optional[str] = None
    haz_imco_char: Optional[str] = None
    haz_imco_sub: Optional[str] = None
    haz_limited_quantities: Optional[str] = None
    haz_marine_pollutant: Optional[str] = None
    haz_material_condition: Optional[str] = None
    haz_mfag: Optional[str] = None
    haz_neq: Optional[str] = None
    haz_nett_weight: Optional[str] = None
    haz_package_type: Optional[str] = None
    haz_pack_grp: Optional[str] = None
    haz_page: Optional[str] = None
    haz_page_no: Optional[str] = None
    haz_pieces: Optional[str] = None
    haz_psn: Optional[str] = None
    haz_stowage_level: Optional[str] = None
    haz_stowage_position: Optional[str] = None
    haz_text: Optional[str] = None
    haz_text_no: Optional[str] = None
    haz_transport_category: Optional[str] = None
    haz_tunnel_code: Optional[str] = None
    haz_unno: Optional[str] = None
    haz_u_npacking_code: Optional[str] = None
    job_id: Optional[str] = None
    kgs_weight_nett: Optional[str] = None
    kgs_wgt: Optional[str] = None
    known_shipper: Optional[str] = None
    lbs_chg: Optional[str] = None
    lbs_vol: Optional[str] = None
    lbs_weight_nett: Optional[str] = None
    lbs_wgt: Optional[str] = None
    line_no: Optional[str] = None
    loading_meters: Optional[str] = None
    marks: Optional[str] = None
    order_no: Optional[str] = None
    package_type: Optional[str] = None
    pallets: Optional[str] = None
    pe_crn: Optional[str] = None
    pieces: Optional[str] = None
    pod_date: Optional[str] = None
    pod_signature: Optional[str] = None
    pod_time: Optional[str] = None
    product_code: Optional[str] = None
    product_desc: Optional[str] = None
    service_failure: Optional[str] = None
    shippers_ref: Optional[str] = None
    sku: Optional[str] = None
    special_instr: Optional[str] = None
    vol_wgt: Optional[str] = None
    wgt_type: Optional[str] = None
    whs_locator: Optional[str] = None
    whs_reference: Optional[str] = None

    def to_dict(self) -> dict:
        result: dict = {}
        result["awb-add1"] = from_union([from_str, from_none], self.awb_add1)
        result["awb-add2"] = from_union([from_str, from_none], self.awb_add2)
        result["awb-add3"] = from_union([from_str, from_none], self.awb_add3)
        result["bill-of-lading"] = from_union([from_str, from_none], self.bill_of_lading)
        result["call-off-ref"] = from_union([from_str, from_none], self.call_off_ref)
        result["cargo-currency"] = from_union([from_str, from_none], self.cargo_currency)
        result["cargo-desc"] = from_union([from_str, from_none], self.cargo_desc)
        result["cargo-value"] = from_union([from_str, from_none], self.cargo_value)
        result["chg-wgt"] = from_union([from_str, from_none], self.chg_wgt)
        result["commodity-item-no"] = from_union([from_str, from_none], self.commodity_item_no)
        result["consignee"] = from_union([from_str, from_none], self.consignee)
        result["consignee-ctry"] = from_union([from_str, from_none], self.consignee_ctry)
        result["consignee-name"] = from_union([from_str, from_none], self.consignee_name)
        result["consignee-town"] = from_union([from_str, from_none], self.consignee_town)
        result["consignor"] = from_union([from_str, from_none], self.consignor)
        result["consignor-ctry"] = from_union([from_str, from_none], self.consignor_ctry)
        result["consignor-name"] = from_union([from_str, from_none], self.consignor_name)
        result["consignor-town"] = from_union([from_str, from_none], self.consignor_town)
        result["consolidator"] = from_union([from_str, from_none], self.consolidator)
        result["contact-name"] = from_union([from_str, from_none], self.contact_name)
        result["contacts-ref"] = from_union([from_str, from_none], self.contacts_ref)
        result["contact-telephone"] = from_union([from_str, from_none], self.contact_telephone)
        result["courier-payee"] = from_union([from_str, from_none], self.courier_payee)
        result["credit-letter-text"] = from_union([from_str, from_none], self.credit_letter_text)
        result["cube"] = from_union([from_str, from_none], self.cube)
        result["cube-type"] = from_union([from_str, from_none], self.cube_type)
        result["delivery-date"] = from_union([from_str, from_none], self.delivery_date)
        result["entered-cube"] = from_union([from_str, from_none], self.entered_cube)
        result["entered-wgt"] = from_union([from_str, from_none], self.entered_wgt)
        result["failure-comment"] = from_union([from_str, from_none], self.failure_comment)
        result["ft-cube"] = from_union([from_str, from_none], self.ft_cube)
        result["goods-received"] = from_union([from_str, from_none], self.goods_received)
        result["handling-text"] = from_union([from_str, from_none], self.handling_text)
        result["har-cargo"] = from_union([from_str, from_none], self.har_cargo)
        result["haz-contact-fax"] = from_union([from_str, from_none], self.haz_contact_fax)
        result["haz-contact-name"] = from_union([from_str, from_none], self.haz_contact_name)
        result["haz-contact-telephone"] = from_union([from_str, from_none], self.haz_contact_telephone)
        result["haz-ems"] = from_union([from_str, from_none], self.haz_ems)
        result["haz-extraChar-1"] = from_union([from_str, from_none], self.haz_extra_char_1)
        result["haz-extraChar-2"] = from_union([from_str, from_none], self.haz_extra_char_2)
        result["haz-extraChar-3"] = from_union([from_str, from_none], self.haz_extra_char_3)
        result["haz-extraChar-4"] = from_union([from_str, from_none], self.haz_extra_char_4)
        result["haz-extraChar-5"] = from_union([from_str, from_none], self.haz_extra_char_5)
        result["haz-extraChar-6"] = from_union([from_str, from_none], self.haz_extra_char_6)
        result["haz-extraChar-7"] = from_union([from_str, from_none], self.haz_extra_char_7)
        result["haz-extraChar-8"] = from_union([from_str, from_none], self.haz_extra_char_8)
        result["haz-extraChar-9"] = from_union([from_str, from_none], self.haz_extra_char_9)
        result["haz-extraDate-1"] = from_union([from_str, from_none], self.haz_extra_date_1)
        result["haz-extraDate-2"] = from_union([from_str, from_none], self.haz_extra_date_2)
        result["haz-extraDate-3"] = from_union([from_str, from_none], self.haz_extra_date_3)
        result["haz-extraDate-4"] = from_union([from_str, from_none], self.haz_extra_date_4)
        result["haz-extraDate-5"] = from_union([from_str, from_none], self.haz_extra_date_5)
        result["haz-extraDate-6"] = from_union([from_str, from_none], self.haz_extra_date_6)
        result["haz-extraDate-7"] = from_union([from_str, from_none], self.haz_extra_date_7)
        result["haz-extraDate-8"] = from_union([from_str, from_none], self.haz_extra_date_8)
        result["haz-extraDate-9"] = from_union([from_str, from_none], self.haz_extra_date_9)
        result["haz-extraInt-1"] = from_union([from_str, from_none], self.haz_extra_int_1)
        result["haz-extraInt-2"] = from_union([from_str, from_none], self.haz_extra_int_2)
        result["haz-extraInt-3"] = from_union([from_str, from_none], self.haz_extra_int_3)
        result["haz-extraInt-4"] = from_union([from_str, from_none], self.haz_extra_int_4)
        result["haz-extraInt-5"] = from_union([from_str, from_none], self.haz_extra_int_5)
        result["haz-extraInt-6"] = from_union([from_str, from_none], self.haz_extra_int_6)
        result["haz-extraInt-7"] = from_union([from_str, from_none], self.haz_extra_int_7)
        result["haz-extraInt-8"] = from_union([from_str, from_none], self.haz_extra_int_8)
        result["haz-extraInt-9"] = from_union([from_str, from_none], self.haz_extra_int_9)
        result["haz-extraLog-1"] = from_union([from_str, from_none], self.haz_extra_log_1)
        result["haz-extraLog-2"] = from_union([from_str, from_none], self.haz_extra_log_2)
        result["haz-extraLog-3"] = from_union([from_str, from_none], self.haz_extra_log_3)
        result["haz-extraLog-4"] = from_union([from_str, from_none], self.haz_extra_log_4)
        result["haz-extraLog-5"] = from_union([from_str, from_none], self.haz_extra_log_5)
        result["haz-extraLog-6"] = from_union([from_str, from_none], self.haz_extra_log_6)
        result["haz-extraLog-7"] = from_union([from_str, from_none], self.haz_extra_log_7)
        result["haz-extraLog-8"] = from_union([from_str, from_none], self.haz_extra_log_8)
        result["haz-extraLog-9"] = from_union([from_str, from_none], self.haz_extra_log_9)
        result["haz-flashpoint"] = from_union([from_str, from_none], self.haz_flashpoint)
        result["haz-imco"] = from_union([from_str, from_none], self.haz_imco)
        result["haz-imco-char"] = from_union([from_str, from_none], self.haz_imco_char)
        result["haz-imco-sub"] = from_union([from_str, from_none], self.haz_imco_sub)
        result["haz-limited-quantities"] = from_union([from_str, from_none], self.haz_limited_quantities)
        result["haz-marine-pollutant"] = from_union([from_str, from_none], self.haz_marine_pollutant)
        result["haz-material-condition"] = from_union([from_str, from_none], self.haz_material_condition)
        result["haz-mfag"] = from_union([from_str, from_none], self.haz_mfag)
        result["haz-neq"] = from_union([from_str, from_none], self.haz_neq)
        result["haz-nett-weight"] = from_union([from_str, from_none], self.haz_nett_weight)
        result["haz-package-type"] = from_union([from_str, from_none], self.haz_package_type)
        result["haz-pack-grp"] = from_union([from_str, from_none], self.haz_pack_grp)
        result["haz-page"] = from_union([from_str, from_none], self.haz_page)
        result["haz-page-no"] = from_union([from_str, from_none], self.haz_page_no)
        result["haz-pieces"] = from_union([from_str, from_none], self.haz_pieces)
        result["haz-psn"] = from_union([from_str, from_none], self.haz_psn)
        result["haz-stowage-level"] = from_union([from_str, from_none], self.haz_stowage_level)
        result["haz-stowage-position"] = from_union([from_str, from_none], self.haz_stowage_position)
        result["haz-text"] = from_union([from_str, from_none], self.haz_text)
        result["haz-text-no"] = from_union([from_str, from_none], self.haz_text_no)
        result["haz-transport-category"] = from_union([from_str, from_none], self.haz_transport_category)
        result["haz-tunnel-code"] = from_union([from_str, from_none], self.haz_tunnel_code)
        result["haz-unno"] = from_union([from_str, from_none], self.haz_unno)
        result["haz-UNpacking-code"] = from_union([from_str, from_none], self.haz_u_npacking_code)
        result["job-id"] = from_union([from_str, from_none], self.job_id)
        result["kgs-weight-nett"] = from_union([from_str, from_none], self.kgs_weight_nett)
        result["kgs-wgt"] = from_union([from_str, from_none], self.kgs_wgt)
        result["known-shipper"] = from_union([from_str, from_none], self.known_shipper)
        result["lbs-chg"] = from_union([from_str, from_none], self.lbs_chg)
        result["lbs-vol"] = from_union([from_str, from_none], self.lbs_vol)
        result["lbs-weight-nett"] = from_union([from_str, from_none], self.lbs_weight_nett)
        result["lbs-wgt"] = from_union([from_str, from_none], self.lbs_wgt)
        result["line-no"] = from_union([from_str, from_none], self.line_no)
        result["loading-meters"] = from_union([from_str, from_none], self.loading_meters)
        result["marks"] = from_union([from_str, from_none], self.marks)
        result["order-no"] = from_union([from_str, from_none], self.order_no)
        result["package-type"] = from_union([from_str, from_none], self.package_type)
        result["pallets"] = from_union([from_str, from_none], self.pallets)
        result["pe-crn"] = from_union([from_str, from_none], self.pe_crn)
        result["pieces"] = from_union([from_str, from_none], self.pieces)
        result["pod-date"] = from_union([from_str, from_none], self.pod_date)
        result["pod-signature"] = from_union([from_str, from_none], self.pod_signature)
        result["pod-time"] = from_union([from_str, from_none], self.pod_time)
        result["product-code"] = from_union([from_str, from_none], self.product_code)
        result["product-desc"] = from_union([from_str, from_none], self.product_desc)
        result["service-failure"] = from_union([from_str, from_none], self.service_failure)
        result["shippers-ref"] = from_union([from_str, from_none], self.shippers_ref)
        result["sku"] = from_union([from_str, from_none], self.sku)
        result["special-instr"] = from_union([from_str, from_none], self.special_instr)
        result["vol-wgt"] = from_union([from_str, from_none], self.vol_wgt)
        result["wgt-type"] = from_union([from_str, from_none], self.wgt_type)
        result["whs-locator"] = from_union([from_str, from_none], self.whs_locator)
        result["whs-reference"] = from_union([from_str, from_none], self.whs_reference)
        return {k: v for k, v in result.items() if v is not None}

@dataclass
class JobCol:
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    address_3: Optional[str] = None
    address_code: Optional[str] = None
    avoid_times: Optional[str] = None
    bol_received: Optional[str] = None
    checked_by: Optional[str] = None
    checked_date: Optional[str] = None
    close_time: Optional[str] = None
    col_date: Optional[str] = None
    col_no: Optional[str] = None
    col_ref: Optional[str] = None
    col_time: Optional[str] = None
    contact_name: Optional[str] = None
    country_code: Optional[str] = None
    county: Optional[str] = None
    cube: Optional[str] = None
    cube_type: Optional[str] = None
    date_amended: Optional[str] = None
    date_created: Optional[str] = None
    depot: Optional[str] = None
    depot_date: Optional[str] = None
    depot_time: Optional[str] = None
    driver: Optional[str] = None
    driver_mobile: Optional[str] = None
    email: Optional[str] = None
    entered_cube: Optional[str] = None
    entered_weight: Optional[str] = None
    equipment: Optional[str] = None
    extra_details: Optional[str] = None
    failed: Optional[str] = None
    failure_by: Optional[str] = None
    failure_comment: Optional[str] = None
    failure_date: Optional[str] = None
    fax: Optional[str] = None
    ft_cube: Optional[str] = None
    haulage_provider: Optional[str] = None
    haulier: Optional[str] = None
    haulier_ctry: Optional[str] = None
    haulier_name: Optional[str] = None
    haulier_town: Optional[str] = None
    job_id: Optional[str] = None
    kgs_weight_nett: Optional[str] = None
    kgs_wgt: Optional[str] = None
    known_shipper: Optional[str] = None
    lbs_weight_nett: Optional[str] = None
    lbs_wgt: Optional[str] = None
    loading_meters: Optional[str] = None
    name: Optional[str] = None
    num_prints: Optional[str] = None
    open_time: Optional[str] = None
    package_type: Optional[str] = None
    pallets: Optional[str] = None
    pieces: Optional[str] = None
    pod_date: Optional[str] = None
    pod_signature: Optional[str] = None
    pod_time: Optional[str] = None
    postcode: Optional[str] = None
    printed: Optional[str] = None
    product_code: Optional[str] = None
    product_desc: Optional[str] = None
    service_failure: Optional[str] = None
    sys_ref: Optional[str] = None
    sysuser: Optional[str] = None
    sysuser_amended: Optional[str] = None
    telephone: Optional[str] = None
    telex: Optional[str] = None
    time_amended: Optional[str] = None
    time_created: Optional[str] = None
    town: Optional[str] = None
    trailer_number: Optional[str] = None
    vehicle_booked_date: Optional[str] = None
    vehicle_reg: Optional[str] = None
    weight_type: Optional[str] = None
    zone_code: Optional[str] = None

    def to_dict(self) -> dict:
        result: dict = {}
        result["address-1"] = from_union([from_str, from_none], self.address_1)
        result["address-2"] = from_union([from_str, from_none], self.address_2)
        result["address-3"] = from_union([from_str, from_none], self.address_3)
        result["address-code"] = from_union([from_str, from_none], self.address_code)
        result["avoid-times"] = from_union([from_str, from_none], self.avoid_times)
        result["bol-received"] = from_union([from_str, from_none], self.bol_received)
        result["checked-by"] = from_union([from_str, from_none], self.checked_by)
        result["checked-date"] = from_union([from_str, from_none], self.checked_date)
        result["close-time"] = from_union([from_str, from_none], self.close_time)
        result["col-date"] = from_union([from_str, from_none], self.col_date)
        result["col-no"] = from_union([from_str, from_none], self.col_no)
        result["col-ref"] = from_union([from_str, from_none], self.col_ref)
        result["col-time"] = from_union([from_str, from_none], self.col_time)
        result["contact-name"] = from_union([from_str, from_none], self.contact_name)
        result["country-code"] = from_union([from_str, from_none], self.country_code)
        result["county"] = from_union([from_str, from_none], self.county)
        result["cube"] = from_union([from_str, from_none], self.cube)
        result["cube-type"] = from_union([from_str, from_none], self.cube_type)
        result["date-amended"] = from_union([from_str, from_none], self.date_amended)
        result["date-created"] = from_union([from_str, from_none], self.date_created)
        result["depot"] = from_union([from_str, from_none], self.depot)
        result["depot-date"] = from_union([from_str, from_none], self.depot_date)
        result["depot-time"] = from_union([from_str, from_none], self.depot_time)
        result["driver"] = from_union([from_str, from_none], self.driver)
        result["driver-mobile"] = from_union([from_str, from_none], self.driver_mobile)
        result["email"] = from_union([from_str, from_none], self.email)
        result["entered-cube"] = from_union([from_str, from_none], self.entered_cube)
        result["entered-weight"] = from_union([from_str, from_none], self.entered_weight)
        result["equipment"] = from_union([from_str, from_none], self.equipment)
        result["extra-details"] = from_union([from_str, from_none], self.extra_details)
        result["failed"] = from_union([from_str, from_none], self.failed)
        result["failure-by"] = from_union([from_str, from_none], self.failure_by)
        result["failure-comment"] = from_union([from_str, from_none], self.failure_comment)
        result["failure-date"] = from_union([from_str, from_none], self.failure_date)
        result["fax"] = from_union([from_str, from_none], self.fax)
        result["ft-cube"] = from_union([from_str, from_none], self.ft_cube)
        result["haulage-provider"] = from_union([from_str, from_none], self.haulage_provider)
        result["haulier"] = from_union([from_str, from_none], self.haulier)
        result["haulier-ctry"] = from_union([from_str, from_none], self.haulier_ctry)
        result["haulier-name"] = from_union([from_str, from_none], self.haulier_name)
        result["haulier-town"] = from_union([from_str, from_none], self.haulier_town)
        result["job-id"] = from_union([from_str, from_none], self.job_id)
        result["kgs-weight-nett"] = from_union([from_str, from_none], self.kgs_weight_nett)
        result["kgs-wgt"] = from_union([from_str, from_none], self.kgs_wgt)
        result["known-shipper"] = from_union([from_str, from_none], self.known_shipper)
        result["lbs-weight-nett"] = from_union([from_str, from_none], self.lbs_weight_nett)
        result["lbs-wgt"] = from_union([from_str, from_none], self.lbs_wgt)
        result["loading-meters"] = from_union([from_str, from_none], self.loading_meters)
        result["name"] = from_union([from_str, from_none], self.name)
        result["num-prints"] = from_union([from_str, from_none], self.num_prints)
        result["open-time"] = from_union([from_str, from_none], self.open_time)
        result["package-type"] = from_union([from_str, from_none], self.package_type)
        result["pallets"] = from_union([from_str, from_none], self.pallets)
        result["pieces"] = from_union([from_str, from_none], self.pieces)
        result["pod-date"] = from_union([from_str, from_none], self.pod_date)
        result["pod-signature"] = from_union([from_str, from_none], self.pod_signature)
        result["pod-time"] = from_union([from_str, from_none], self.pod_time)
        result["postcode"] = from_union([from_str, from_none], self.postcode)
        result["printed"] = from_union([from_str, from_none], self.printed)
        result["product-code"] = from_union([from_str, from_none], self.product_code)
        result["product-desc"] = from_union([from_str, from_none], self.product_desc)
        result["service-failure"] = from_union([from_str, from_none], self.service_failure)
        result["sys-ref"] = from_union([from_str, from_none], self.sys_ref)
        result["sysuser"] = from_union([from_str, from_none], self.sysuser)
        result["sysuser-amended"] = from_union([from_str, from_none], self.sysuser_amended)
        result["telephone"] = from_union([from_str, from_none], self.telephone)
        result["telex"] = from_union([from_str, from_none], self.telex)
        result["time-amended"] = from_union([from_str, from_none], self.time_amended)
        result["time-created"] = from_union([from_str, from_none], self.time_created)
        result["town"] = from_union([from_str, from_none], self.town)
        result["trailer-number"] = from_union([from_str, from_none], self.trailer_number)
        result["vehicle-booked-date"] = from_union([from_str, from_none], self.vehicle_booked_date)
        result["vehicle-reg"] = from_union([from_str, from_none], self.vehicle_reg)
        result["weight-type"] = from_union([from_str, from_none], self.weight_type)
        result["zone-code"] = from_union([from_str, from_none], self.zone_code)
        return {k: v for k, v in result.items() if v is not None}

@dataclass
class JobDel:
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    address_3: Optional[str] = None
    address_code: Optional[str] = None
    avoid_times: Optional[str] = None
    bol_received: Optional[str] = None
    checked_by: Optional[str] = None
    checked_date: Optional[str] = None
    close_time: Optional[str] = None
    contact_name: Optional[str] = None
    country_code: Optional[str] = None
    county: Optional[str] = None
    cube: Optional[str] = None
    cube_type: Optional[str] = None
    date_amended: Optional[str] = None
    date_created: Optional[str] = None
    del_date: Optional[str] = None
    delivery_type: Optional[str] = None
    del_no: Optional[str] = None
    del_ref: Optional[str] = None
    del_time: Optional[str] = None
    depot: Optional[str] = None
    driver: Optional[str] = None
    driver_mobile: Optional[str] = None
    email: Optional[str] = None
    entered_cube: Optional[str] = None
    entered_weight: Optional[str] = None
    equipment: Optional[str] = None
    extra_details: Optional[str] = None
    failed: Optional[str] = None
    failure_by: Optional[str] = None
    failure_comment: Optional[str] = None
    failure_date: Optional[str] = None
    fax: Optional[str] = None
    ft_cube: Optional[str] = None
    haulage_provider: Optional[str] = None
    haulier: Optional[str] = None
    haulier_ctry: Optional[str] = None
    haulier_name: Optional[str] = None
    haulier_town: Optional[str] = None
    job_id: Optional[str] = None
    kgs_weight_nett: Optional[str] = None
    kgs_wgt: Optional[str] = None
    known_shipper: Optional[str] = None
    lbs_weight_nett: Optional[str] = None
    lbs_wgt: Optional[str] = None
    loading_meters: Optional[str] = None
    name: Optional[str] = None
    number_of_prints: Optional[str] = None
    off_quay_date: Optional[str] = None
    off_quay_time: Optional[str] = None
    open_time: Optional[str] = None
    package_type: Optional[str] = None
    pallets: Optional[str] = None
    pieces: Optional[str] = None
    pod_date: Optional[str] = None
    pod_signature: Optional[str] = None
    pod_time: Optional[str] = None
    postcode: Optional[str] = None
    printed: Optional[str] = None
    product_code: Optional[str] = None
    product_desc: Optional[str] = None
    service_failure: Optional[str] = None
    sys_ref: Optional[str] = None
    sysuser: Optional[str] = None
    sysuser_amended: Optional[str] = None
    telephone: Optional[str] = None
    telex: Optional[str] = None
    time_amended: Optional[str] = None
    time_created: Optional[str] = None
    town: Optional[str] = None
    trailer_number: Optional[str] = None
    vehicle_booked_date: Optional[str] = None
    vehicle_reg: Optional[str] = None
    weight_type: Optional[str] = None
    zone_code: Optional[str] = None

    def to_dict(self) -> dict:
        result: dict = {}
        result["address-1"] = from_union([from_str, from_none], self.address_1)
        result["address-2"] = from_union([from_str, from_none], self.address_2)
        result["address-3"] = from_union([from_str, from_none], self.address_3)
        result["address-code"] = from_union([from_str, from_none], self.address_code)
        result["avoid-times"] = from_union([from_str, from_none], self.avoid_times)
        result["bol-received"] = from_union([from_str, from_none], self.bol_received)
        result["checked-by"] = from_union([from_str, from_none], self.checked_by)
        result["checked-date"] = from_union([from_str, from_none], self.checked_date)
        result["close-time"] = from_union([from_str, from_none], self.close_time)
        result["contact-name"] = from_union([from_str, from_none], self.contact_name)
        result["country-code"] = from_union([from_str, from_none], self.country_code)
        result["county"] = from_union([from_str, from_none], self.county)
        result["cube"] = from_union([from_str, from_none], self.cube)
        result["cube-type"] = from_union([from_str, from_none], self.cube_type)
        result["date-amended"] = from_union([from_str, from_none], self.date_amended)
        result["date-created"] = from_union([from_str, from_none], self.date_created)
        result["del-date"] = from_union([from_str, from_none], self.del_date)
        result["delivery-type"] = from_union([from_str, from_none], self.delivery_type)
        result["del-no"] = from_union([from_str, from_none], self.del_no)
        result["del-ref"] = from_union([from_str, from_none], self.del_ref)
        result["del-time"] = from_union([from_str, from_none], self.del_time)
        result["depot"] = from_union([from_str, from_none], self.depot)
        result["driver"] = from_union([from_str, from_none], self.driver)
        result["driver-mobile"] = from_union([from_str, from_none], self.driver_mobile)
        result["email"] = from_union([from_str, from_none], self.email)
        result["entered-cube"] = from_union([from_str, from_none], self.entered_cube)
        result["entered-weight"] = from_union([from_str, from_none], self.entered_weight)
        result["equipment"] = from_union([from_str, from_none], self.equipment)
        result["extra-details"] = from_union([from_str, from_none], self.extra_details)
        result["failed"] = from_union([from_str, from_none], self.failed)
        result["failure-by"] = from_union([from_str, from_none], self.failure_by)
        result["failure-comment"] = from_union([from_str, from_none], self.failure_comment)
        result["failure-date"] = from_union([from_str, from_none], self.failure_date)
        result["fax"] = from_union([from_str, from_none], self.fax)
        result["ft-cube"] = from_union([from_str, from_none], self.ft_cube)
        result["haulage-provider"] = from_union([from_str, from_none], self.haulage_provider)
        result["haulier"] = from_union([from_str, from_none], self.haulier)
        result["haulier-ctry"] = from_union([from_str, from_none], self.haulier_ctry)
        result["haulier-name"] = from_union([from_str, from_none], self.haulier_name)
        result["haulier-town"] = from_union([from_str, from_none], self.haulier_town)
        result["job-id"] = from_union([from_str, from_none], self.job_id)
        result["kgs-weight-nett"] = from_union([from_str, from_none], self.kgs_weight_nett)
        result["kgs-wgt"] = from_union([from_str, from_none], self.kgs_wgt)
        result["known-shipper"] = from_union([from_str, from_none], self.known_shipper)
        result["lbs-weight-nett"] = from_union([from_str, from_none], self.lbs_weight_nett)
        result["lbs-wgt"] = from_union([from_str, from_none], self.lbs_wgt)
        result["loading-meters"] = from_union([from_str, from_none], self.loading_meters)
        result["name"] = from_union([from_str, from_none], self.name)
        result["number-of-prints"] = from_union([from_str, from_none], self.number_of_prints)
        result["off-quay-date"] = from_union([from_str, from_none], self.off_quay_date)
        result["off-quay-time"] = from_union([from_str, from_none], self.off_quay_time)
        result["open-time"] = from_union([from_str, from_none], self.open_time)
        result["package-type"] = from_union([from_str, from_none], self.package_type)
        result["pallets"] = from_union([from_str, from_none], self.pallets)
        result["pieces"] = from_union([from_str, from_none], self.pieces)
        result["pod-date"] = from_union([from_str, from_none], self.pod_date)
        result["pod-signature"] = from_union([from_str, from_none], self.pod_signature)
        result["pod-time"] = from_union([from_str, from_none], self.pod_time)
        result["postcode"] = from_union([from_str, from_none], self.postcode)
        result["printed"] = from_union([from_str, from_none], self.printed)
        result["product-code"] = from_union([from_str, from_none], self.product_code)
        result["product-desc"] = from_union([from_str, from_none], self.product_desc)
        result["service-failure"] = from_union([from_str, from_none], self.service_failure)
        result["sys-ref"] = from_union([from_str, from_none], self.sys_ref)
        result["sysuser"] = from_union([from_str, from_none], self.sysuser)
        result["sysuser-amended"] = from_union([from_str, from_none], self.sysuser_amended)
        result["telephone"] = from_union([from_str, from_none], self.telephone)
        result["telex"] = from_union([from_str, from_none], self.telex)
        result["time-amended"] = from_union([from_str, from_none], self.time_amended)
        result["time-created"] = from_union([from_str, from_none], self.time_created)
        result["town"] = from_union([from_str, from_none], self.town)
        result["trailer-number"] = from_union([from_str, from_none], self.trailer_number)
        result["vehicle-booked-date"] = from_union([from_str, from_none], self.vehicle_booked_date)
        result["vehicle-reg"] = from_union([from_str, from_none], self.vehicle_reg)
        result["weight-type"] = from_union([from_str, from_none], self.weight_type)
        result["zone-code"] = from_union([from_str, from_none], self.zone_code)
        return {k: v for k, v in result.items() if v is not None}

@dataclass
class JobDim:

    cube: Optional[str] = None
    cube_type: Optional[str] = None
    dim_no: Optional[str] = None
    entered_cube: Optional[str] = None
    entered_height: Optional[str] = None
    entered_length: Optional[str] = None
    entered_unit_type: Optional[str] = None
    entered_weight: Optional[str] = None
    entered_width: Optional[str] = None
    ft_cube: Optional[str] = None
    height: Optional[str] = None
    job_id: Optional[str] = None
    kgs_weight_nett: Optional[str] = None
    kgs_wgt: Optional[str] = None
    lbs_weight_nett: Optional[str] = None
    lbs_wgt: Optional[str] = None
    length: Optional[str] = None
    line_no: Optional[str] = None
    package_type: Optional[str] = None
    pieces: Optional[str] = None
    weight_type: Optional[str] = None
    width: Optional[str] = None


    def to_dict(self) -> dict:
        result: dict = {}
        result["cube"] = from_union([from_str, from_none], self.cube)
        result["cube-type"] = from_union([from_str, from_none], self.cube_type)
        result["dim-no"] = from_union([from_str, from_none], self.dim_no)
        result["entered-cube"] = from_union([from_str, from_none], self.entered_cube)
        result["entered-height"] = from_union([from_str, from_none], self.entered_height)
        result["entered-length"] = from_union([from_str, from_none], self.entered_length)
        result["entered-unit-type"] = from_union([from_str, from_none], self.entered_unit_type)
        result["entered-weight"] = from_union([from_str, from_none], self.entered_weight)
        result["entered-width"] = from_union([from_str, from_none], self.entered_width)
        result["ft-cube"] = from_union([from_str, from_none], self.ft_cube)
        result["height"] = from_union([from_str, from_none], self.height)
        result["job-id"] = from_union([from_str, from_none], self.job_id)
        result["kgs-weight-nett"] = from_union([from_str, from_none], self.kgs_weight_nett)
        result["kgs-wgt"] = from_union([from_str, from_none], self.kgs_wgt)
        result["lbs-weight-nett"] = from_union([from_str, from_none], self.lbs_weight_nett)
        result["lbs-wgt"] = from_union([from_str, from_none], self.lbs_wgt)
        result["length"] = from_union([from_str, from_none], self.length)
        result["line-no"] = from_union([from_str, from_none], self.line_no)
        result["package-type"] = from_union([from_str, from_none], self.package_type)
        result["pieces"] = from_union([from_str, from_none], self.pieces)
        result["weight-type"] = from_union([from_str, from_none], self.weight_type)
        result["width"] = from_union([from_str, from_none], self.width)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class Address:
    acc_manager: Optional[str] = None
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    address_3: Optional[str] = None
    address_code: Optional[str] = None
    aeo_ref: Optional[str] = None
    allow_tracking: Optional[str] = None
    analysis_code_1: Optional[str] = None
    analysis_code_2: Optional[str] = None
    analysis_code_3: Optional[str] = None
    analysis_code_4: Optional[str] = None
    auto_pre_alert: Optional[str] = None
    avoid_times: Optional[str] = None
    category: Optional[str] = None
    closing_time: Optional[str] = None
    compregno: Optional[str] = None
    cops_req: Optional[str] = None
    country_code: Optional[str] = None
    county: Optional[str] = None
    courier_discount_amount: Optional[str] = None
    courier_discount_perc: Optional[str] = None
    create_tdni_file: Optional[str] = None
    crn: Optional[str] = None
    currency_code: Optional[str] = None
    customs_id: Optional[str] = None
    data_trans: Optional[str] = None
    date_amended: Optional[str] = None
    date_created: Optional[str] = None
    defer_auth: Optional[str] = None
    deferment_number: Optional[str] = None
    edi_file_location: Optional[str] = None
    email: Optional[str] = None
    eori_no: Optional[str] = None
    fax: Optional[str] = None
    group_code: Optional[str] = None
    guar_code: Optional[str] = None
    guar_no: Optional[str] = None
    guar_not_valid: Optional[str] = None
    gvs1: Optional[str] = None
    gvs2: Optional[str] = None
    gvs3: Optional[str] = None
    haulier: Optional[str] = None
    ins_ind: Optional[str] = None
    ins_perc: Optional[str] = None
    inter_company_code: Optional[str] = None
    inter_dept: Optional[str] = None
    inter_office: Optional[str] = None
    intrastat: Optional[str] = None
    intrastat_import: Optional[str] = None
    inv_address: Optional[str] = None
    invoice_agent: Optional[str] = None
    invoice_format: Optional[str] = None
    keyname: Optional[str] = None
    known_expiry: Optional[str] = None
    known_shipper: Optional[str] = None
    memo1: Optional[str] = None
    memo2: Optional[str] = None
    name: Optional[str] = None
    opening_time: Optional[str] = None
    payment_method: Optional[str] = None
    postcode: Optional[str] = None
    potential: Optional[str] = None
    private_notes: Optional[str] = None
    prof_share_basis: Optional[str] = None
    prof_share_perc: Optional[str] = None
    prof_share_perc_2: Optional[str] = None
    public_notes: Optional[str] = None
    reg_address_1: Optional[str] = None
    reg_address_2: Optional[str] = None
    reg_address_3: Optional[str] = None
    reg_county: Optional[str] = None
    reg_postcode: Optional[str] = None
    reg_town: Optional[str] = None
    reg_vat_country_code: Optional[str] = None
    sale_person: Optional[str] = None
    scac_code: Optional[str] = None
    signatory: Optional[str] = None
    size_of_company: Optional[str] = None
    sysuser: Optional[str] = None
    sysuser_amended: Optional[str] = None
    telephone: Optional[str] = None
    telex: Optional[str] = None
    time_amended: Optional[str] = None
    time_created: Optional[str] = None
    town: Optional[str] = None
    u_address: Optional[str] = None
    vatregno: Optional[str] = None
    vdi: Optional[str] = None
    web_url: Optional[str] = None
    zone: Optional[str] = None

    def to_dict(self) -> dict:
        result: dict = {}
        result["acc-manager"] = from_union([from_str, from_none], self.acc_manager)
        result["address-1"] = from_union([from_str, from_none], self.address_1)
        result["address-2"] = from_union([from_str, from_none], self.address_2)
        result["address-3"] = from_union([from_str, from_none], self.address_3)
        result["address-code"] = from_union([from_str, from_none], self.address_code)
        result["aeo-ref"] = from_union([from_str, from_none], self.aeo_ref)
        result["allow-tracking"] = from_union([from_str, from_none], self.allow_tracking)
        result["analysis-code-1"] = from_union([from_str, from_none], self.analysis_code_1)
        result["analysis-code-2"] = from_union([from_str, from_none], self.analysis_code_2)
        result["analysis-code-3"] = from_union([from_str, from_none], self.analysis_code_3)
        result["analysis-code-4"] = from_union([from_str, from_none], self.analysis_code_4)
        result["auto-pre-alert"] = from_union([from_str, from_none], self.auto_pre_alert)
        result["avoid-times"] = from_union([from_str, from_none], self.avoid_times)
        result["category"] = from_union([from_str, from_none], self.category)
        result["closing-time"] = from_union([from_str, from_none], self.closing_time)
        result["compregno"] = from_union([from_str, from_none], self.compregno)
        result["cops-req"] = from_union([from_str, from_none], self.cops_req)
        result["country-code"] = from_union([from_str, from_none], self.country_code)
        result["county"] = from_union([from_str, from_none], self.county)
        result["courier-discount-amount"] = from_union([from_str, from_none], self.courier_discount_amount)
        result["courier-discount-perc"] = from_union([from_str, from_none], self.courier_discount_perc)
        result["create-tdni-file"] = from_union([from_str, from_none], self.create_tdni_file)
        result["CRN"] = from_union([from_str, from_none], self.crn)
        result["currency-code"] = from_union([from_str, from_none], self.currency_code)
        result["customs-id"] = from_union([from_str, from_none], self.customs_id)
        result["data-trans"] = from_union([from_str, from_none], self.data_trans)
        result["date-amended"] = from_union([from_str, from_none], self.date_amended)
        result["date-created"] = from_union([from_str, from_none], self.date_created)
        result["defer-auth"] = from_union([from_str, from_none], self.defer_auth)
        result["deferment-number"] = from_union([from_str, from_none], self.deferment_number)
        result["edi-file-location"] = from_union([from_str, from_none], self.edi_file_location)
        result["email"] = from_union([from_str, from_none], self.email)
        result["eori-no"] = from_union([from_str, from_none], self.eori_no)
        result["fax"] = from_union([from_str, from_none], self.fax)
        result["group-code"] = from_union([from_str, from_none], self.group_code)
        result["guar-code"] = from_union([from_str, from_none], self.guar_code)
        result["guar-no"] = from_union([from_str, from_none], self.guar_no)
        result["guar-not-valid"] = from_union([from_str, from_none], self.guar_not_valid)
        result["gvs1"] = from_union([from_str, from_none], self.gvs1)
        result["gvs2"] = from_union([from_str, from_none], self.gvs2)
        result["gvs3"] = from_union([from_str, from_none], self.gvs3)
        result["haulier"] = from_union([from_str, from_none], self.haulier)
        result["ins-ind"] = from_union([from_str, from_none], self.ins_ind)
        result["ins-perc"] = from_union([from_str, from_none], self.ins_perc)
        result["inter-company-code"] = from_union([from_str, from_none], self.inter_company_code)
        result["inter-dept"] = from_union([from_str, from_none], self.inter_dept)
        result["inter-office"] = from_union([from_str, from_none], self.inter_office)
        result["intrastat"] = from_union([from_str, from_none], self.intrastat)
        result["intrastat-import"] = from_union([from_str, from_none], self.intrastat_import)
        result["inv-address"] = from_union([from_str, from_none], self.inv_address)
        result["invoice-agent"] = from_union([from_str, from_none], self.invoice_agent)
        result["invoice-format"] = from_union([from_str, from_none], self.invoice_format)
        result["keyname"] = from_union([from_str, from_none], self.keyname)
        result["known-expiry"] = from_union([from_str, from_none], self.known_expiry)
        result["known-shipper"] = from_union([from_str, from_none], self.known_shipper)
        result["memo1"] = from_union([from_str, from_none], self.memo1)
        result["memo2"] = from_union([from_str, from_none], self.memo2)
        result["name"] = from_union([from_str, from_none], self.name)
        result["opening-time"] = from_union([from_str, from_none], self.opening_time)
        result["payment-method"] = from_union([from_str, from_none], self.payment_method)
        result["postcode"] = from_union([from_str, from_none], self.postcode)
        result["potential"] = from_union([from_str, from_none], self.potential)
        result["private-notes"] = from_union([from_str, from_none], self.private_notes)
        result["prof-share-basis"] = from_union([from_str, from_none], self.prof_share_basis)
        result["prof-share-perc"] = from_union([from_str, from_none], self.prof_share_perc)
        result["prof-share-perc-2"] = from_union([from_str, from_none], self.prof_share_perc_2)
        result["public-notes"] = from_union([from_str, from_none], self.public_notes)
        result["reg-address-1"] = from_union([from_str, from_none], self.reg_address_1)
        result["reg-address-2"] = from_union([from_str, from_none], self.reg_address_2)
        result["reg-address-3"] = from_union([from_str, from_none], self.reg_address_3)
        result["reg-county"] = from_union([from_str, from_none], self.reg_county)
        result["reg-postcode"] = from_union([from_str, from_none], self.reg_postcode)
        result["reg-town"] = from_union([from_str, from_none], self.reg_town)
        result["regVATCountryCode"] = from_union([from_str, from_none], self.reg_vat_country_code)
        result["sale-person"] = from_union([from_str, from_none], self.sale_person)
        result["SCAC-code"] = from_union([from_str, from_none], self.scac_code)
        result["signatory"] = from_union([from_str, from_none], self.signatory)
        result["size-of-company"] = from_union([from_str, from_none], self.size_of_company)
        result["sysuser"] = from_union([from_str, from_none], self.sysuser)
        result["sysuser-amended"] = from_union([from_str, from_none], self.sysuser_amended)
        result["telephone"] = from_union([from_str, from_none], self.telephone)
        result["telex"] = from_union([from_str, from_none], self.telex)
        result["time-amended"] = from_union([from_str, from_none], self.time_amended)
        result["time-created"] = from_union([from_str, from_none], self.time_created)
        result["town"] = from_union([from_str, from_none], self.town)
        result["u-address"] = from_union([from_str, from_none], self.u_address)
        result["vatregno"] = from_union([from_str, from_none], self.vatregno)
        result["vdi"] = from_union([from_str, from_none], self.vdi)
        result["web-url"] = from_union([from_str, from_none], self.web_url)
        result["zone"] = from_union([from_str, from_none], self.zone)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class Tables:
    job_hdr: Optional[JobHdr] = None
    job_line: Optional[List[JobLine]] = None
    job_dims: Optional[List[JobDim]] = None
    job_del: Optional[List[JobDel]] = None
    job_col: Optional[List[JobCol]] = None
    address: Optional[Address] = None
    doc_adds: Optional[List[DocAdd]] = None
    rec_chg: Optional[List[RecChg]] = None
    rec_jny: Optional[List[RecJny]] = None

    def __post_init__(self):
        self.job_hdr = JobHdr()
        self.job_line = []
        self.job_dims = []
        self.job_del = []
        self.job_col = []
        self.address = Address()
        self.doc_adds = []
        self.rec_chg = []
        self.rec_jny = []

    def to_dict(self) -> dict:
        result: dict = {}
        result["job-hdr"] = from_union([lambda x: to_class(JobHdr, x), from_none], self.job_hdr)
        result["_LIST_job-line_LIST"] = from_union([lambda x: from_list(lambda x: to_class(JobLine, x), x), from_none], self.job_line)
        result["_LIST_job-dims_LIST"] = from_union([lambda x: from_list(lambda x: to_class(JobDim, x), x), from_none], self.job_dims)
        result["_LIST_job-col_LIST"] = from_union([lambda x: from_list(lambda x: to_class(JobCol, x), x), from_none], self.job_col)
        result["_LIST_job-del_LIST"] = from_union([lambda x: from_list(lambda x: to_class(JobDel, x), x), from_none], self.job_del)
        result["address"] = from_union([lambda x: to_class(Address, x), from_none], self.address)
        result["_LIST_doc-adds_LIST"] = from_union([lambda x: from_list(lambda x: to_class(DocAdd, x), x), from_none], self.doc_adds)
        result["_LIST_rec-chg_LIST"] = from_union([lambda x: from_list(lambda x: to_class(RecChg, x), x), from_none], self.rec_chg)
        result["_LIST_rec-jny_LIST"] = from_union([lambda x: from_list(lambda x: to_class(RecJny, x), x), from_none], self.rec_jny)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class Isledi:
    context: Optional[ISLEDIContext] = None
    tables: Optional[Tables] = None

    def __post_init__(self):
        self.context = ISLEDIContext()
        self.tables = Tables()

    def to_dict(self) -> dict:
        result: dict = {}
        result["Context"] = from_union([lambda x: to_class(ISLEDIContext, x), from_none], self.context)
        result["Tables"] = from_union([lambda x: to_class(Tables, x), from_none], self.tables)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class Combined:
    isledi: Optional[Isledi] = None

    def __post_init__(self):
        self.isledi = Isledi()

    def to_dict(self) -> dict:
        result: dict = {}
        result["ISLEDI"] = from_union([lambda x: to_class(Isledi, x), from_none], self.isledi)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class Interface:
    pass

    def to_dict(self) -> dict:
        result: dict = {}
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class MSEDIIMPORTSContext:
    interface: Optional[Interface] = None
    arrived: Optional[str] = None
    send_msg: Optional[str] = None

    def __post_init__(self):
        self.interface = Interface()
        # self.arrived = "false"
        # self.send_msg = "true"
        

    def to_dict(self) -> dict:
        result: dict = {}
        result["arrived"] = from_union([from_str, from_none], self.arrived)
        result["send-msg"] = from_union([from_str, from_none], self.send_msg)
        result["INTERFACE"] = from_union([lambda x: to_class(Interface, x), from_none], self.interface)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EDICdecItmAI:
    rec_type: Optional[str] = None
    item_no: Optional[str] = None
    ai_no: Optional[str] = None
    item_ai_stmt: Optional[str] = None
    item_ai_stmt_lng: Optional[str] = None
    item_ai_stmt_txt: Optional[str] = None
    interface: Optional[Interface] = None

    def to_dict(self) -> dict:
        result: dict = {}
        result["rec_type"] = from_union([from_str, from_none], self.rec_type)
        result["item_no"] = from_union([from_str, from_none], self.item_no)
        result["ai_no"] = from_union([from_str, from_none], self.ai_no)
        result["item_ai_stmt"] = from_union([from_str, from_none], self.item_ai_stmt)
        result["item_ai_stmt_lng"] = from_union([from_str, from_none], self.item_ai_stmt_lng)
        result["item_ai_stmt_txt"] = from_union([from_str, from_none], self.item_ai_stmt_txt)
        result["INTERFACE"] = from_union([lambda x: to_class(Interface, x), from_none], self.interface)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EDICdecItmDoc:
    item_no: Optional[str] = None
    doc_no: Optional[str] = None
    item_doc_code: Optional[str] = None
    item_doc_qty: Optional[str] = None
    item_doc_ref: Optional[str] = None
    item_doc_status: Optional[str] = None
    interface: Optional[Interface] = None

    def to_dict(self) -> dict:
        result: dict = {}
        result["item_no"] = from_union([from_str, from_none], self.item_no)
        result["doc_no"] = from_union([from_str, from_none], self.doc_no)
        result["item_doc_code"] = from_union([from_str, from_none], self.item_doc_code)
        result["item_doc_qty"] = from_union([from_str, from_none], self.item_doc_qty)
        result["item_doc_ref"] = from_union([from_str, from_none], self.item_doc_ref)
        result["item_doc_status"] = from_union([from_str, from_none], self.item_doc_status)
        result["INTERFACE"] = from_union([lambda x: to_class(Interface, x), from_none], self.interface)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EDICdecItmPdc:
    item_no: Optional[str] = None
    pdc_no: Optional[str] = None
    prev_doc_class: Optional[str] = None
    prev_doc_ref: Optional[str] = None
    prev_doc_type: Optional[str] = None
    interface: Optional[Interface] = None

    def __post_init__(self):
        self.interface = Interface()

    def to_dict(self) -> dict:
        result: dict = {}
        result["item_no"] = from_union([from_str, from_none], self.item_no)
        result["pdc_no"] = from_union([from_str, from_none], self.pdc_no)
        result["prev_doc_class"] = from_union([from_str, from_none], self.prev_doc_class)
        result["prev_doc_ref"] = from_union([from_str, from_none], self.prev_doc_ref)
        result["prev_doc_type"] = from_union([from_str, from_none], self.prev_doc_type)
        result["INTERFACE"] = from_union([lambda x: to_class(Interface, x), from_none], self.interface)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EDICdecItmCnt:
    item_no: Optional[str] = None
    cnt_no: Optional[str] = None
    cntr_no: Optional[str] = None
    
    def __post_init__(self):
        self.interface = Interface()

    def to_dict(self) -> dict:
        result: dict = {}
        result["item_no"] = from_union([from_str, from_none], self.item_no)
        result["cnt_no"] = from_union([from_str, from_none], self.cnt_no)
        result["cntr_no"] = from_union([from_str, from_none], self.cntr_no)
        return {k: v for k, v in result.items() if v is not None}

@dataclass
class EDICdecItmPkg:
    item_no: Optional[str] = None
    pkg_no: Optional[str] = None
    pkg_count: Optional[str] = None
    pkg_kind: Optional[str] = None
    pkg_marks: Optional[str] = None
    pkg_marks_lng: Optional[str] = None
    interface: Optional[Interface] = None

    def __post_init__(self):
        self.interface = Interface()

    def to_dict(self) -> dict:
        result: dict = {}
        result["item_no"] = from_union([from_str, from_none], self.item_no)
        result["pkg_no"] = from_union([from_str, from_none], self.pkg_no)
        result["pkg_count"] = from_union([from_str, from_none], self.pkg_count)
        result["pkg_kind"] = from_union([from_str, from_none], self.pkg_kind)
        result["pkg_marks"] = from_union([from_str, from_none], self.pkg_marks)
        result["pkg_marks_lng"] = from_union([from_str, from_none], self.pkg_marks_lng)
        result["INTERFACE"] = from_union([lambda x: to_class(Interface, x), from_none], self.interface)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EDICdecItmTax:
    item_no: Optional[str] = None
    mop_code: Optional[str] = None
    tax_no: Optional[str] = None
    tax_rate_id: Optional[str] = None
    tty_code: Optional[str] = None
    interface: Optional[Interface] = None

    def __post_init__(self):
        self.interface = Interface()

    def to_dict(self) -> dict:
        result: dict = {}
        result["item_no"] = from_union([from_str, from_none], self.item_no)
        result["mop_code"] = from_union([from_str, from_none], self.mop_code)
        result["tax_no"] = from_union([from_str, from_none], self.tax_no)
        result["tax_rate_id"] = from_union([from_str, from_none], self.tax_rate_id)
        result["tty_code"] = from_union([from_str, from_none], self.tty_code)
        result["INTERFACE"] = from_union([lambda x: to_class(Interface, x), from_none], self.interface)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class CustomsItem:
    commodity_desc: Optional[str] = None
    item_no: Optional[str] = None
    pkgs: Optional[str] = None
    qty_code: Optional[str] = None
    interface: Optional[Interface] = None
    edi_cdec_itm_ai: Optional[List[EDICdecItmAI]] = None
    edi_cdec_itm_doc: Optional[List[EDICdecItmDoc]] = None
    edi_cdec_itm_pkg: Optional[EDICdecItmPkg] = None
    edi_cdec_itm_pdc: Optional[EDICdecItmPdc] = None
    edi_cdec_itm_tax: Optional[List[EDICdecItmTax]] = None

    def __post_init__(self):
        self.interface = Interface()
        self.edi_cdec_itm_ai = []
        self.edi_cdec_itm_doc = []
        self.edi_cdec_itm_pkg = EDICdecItmPkg()
        self.edi_cdec_itm_pdc = EDICdecItmPdc()
        self.edi_cdec_itm_tax = []

    def to_dict(self) -> dict:
        result: dict = {}
        result["commodity_desc"] = from_union([from_str, from_none], self.commodity_desc)
        result["item_no"] = from_union([from_str, from_none], self.item_no)
        result["pkgs"] = from_union([from_str, from_none], self.pkgs)
        result["qty_code"] = from_union([from_str, from_none], self.qty_code)
        result["INTERFACE"] = from_union([lambda x: to_class(Interface, x), from_none], self.interface)
        result["_LIST_EDI_CDEC_ITM_AI_LIST"] = from_union([lambda x: from_list(lambda x: to_class(EDICdecItmAI, x), x), from_none], self.edi_cdec_itm_ai)
        result["_LIST_EDI_CDEC_ITM_DOC_LIST"] = from_union([lambda x: from_list(lambda x: to_class(EDICdecItmDoc, x), x), from_none], self.edi_cdec_itm_doc)
        result["EDI_CDEC_ITM_PKG"] = from_union([lambda x: to_class(EDICdecItmPkg, x), from_none], self.edi_cdec_itm_pkg)
        result["EDI_CDEC_ITM_PDC"] = from_union([lambda x: to_class(EDICdecItmPdc, x), from_none], self.edi_cdec_itm_pdc)
        result["_LIST_EDI_CDEC_ITM_TAX_LIST"] = from_union([lambda x: from_list(lambda x: to_class(EDICdecItmTax, x), x), from_none], self.edi_cdec_itm_tax)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EDICdecItm:
    base_cmdty_code: Optional[str] = None
    cpc: Optional[str] = None
    gds_desc: Optional[str] = None
    item_gross_mass: Optional[str] = None
    item_net_mass: Optional[str] = None
    item_no: Optional[str] = None
    item_orig_cntry: Optional[str] = None
    item_prc_ac: Optional[str] = None
    item_stat_val_dc: Optional[str] = None
    item_supp_units: Optional[str] = None
    preference: Optional[str] = None
    taric_cmdty_code: Optional[str] = None
    val_adjt_code: Optional[str] = None
    val_mthd_code: Optional[str] = None
    interface: Optional[Interface] = None

    def __post_init__(self):
        self.interface = Interface()

    def to_dict(self) -> dict:
        result: dict = {}
        result["base_cmdty_code"] = from_union([from_str, from_none], self.base_cmdty_code)
        result["cpc"] = from_union([from_str, from_none], self.cpc)
        result["gds_desc"] = from_union([from_str, from_none], self.gds_desc)
        result["item_gross_mass"] = from_union([from_str, from_none], self.item_gross_mass)
        result["item_net_mass"] = from_union([from_str, from_none], self.item_net_mass)
        result["item_no"] = from_union([from_str, from_none], self.item_no)
        result["item_orig_cntry"] = from_union([from_str, from_none], self.item_orig_cntry)
        result["item_prc_ac"] = from_union([from_str, from_none], self.item_prc_ac)
        result["item_stat_val_dc"] = from_union([from_str, from_none], self.item_stat_val_dc)
        result["item_supp_units"] = from_union([from_str, from_none], self.item_supp_units)
        result["preference"] = from_union([from_str, from_none], self.preference)
        result["taric_cmdty_code"] = from_union([from_str, from_none], self.taric_cmdty_code)
        result["val_adjt_code"] = from_union([from_str, from_none], self.val_adjt_code)
        result["val_mthd_code"] = from_union([from_str, from_none], self.val_mthd_code)
        result["INTERFACE"] = from_union([lambda x: to_class(Interface, x), from_none], self.interface)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class Customs:
    customs_ref: Optional[str] = None
    mfrt_job_id: Optional[str] = None
    consignor_code: Optional[str] = None
    importer_code: Optional[str] = None
    agent_code: Optional[str] = None
    consignor_name: Optional[str] = None
    consignor_address: Optional[List[str]] = None
    consignor_county: Optional[str] = None
    consignor_country: Optional[str] = None
    enttype: Optional[str] = None
    importer_name: Optional[str] = None
    importer_address: Optional[List[str]] = None
    importer_county: Optional[str] = None
    importer_country: Optional[str] = None
    importer_vatregn: Optional[str] = None
    agent_name: Optional[str] = None
    agent_address: Optional[List[str]] = None
    agent_county: Optional[str] = None
    agent_country: Optional[str] = None
    agent_vatregn: Optional[str] = None
    agent_tel: Optional[str] = None
    pkgs: Optional[str] = None
    gross_weight: Optional[str] = None
    port_loading: Optional[str] = None
    country_dispatch: Optional[str] = None
    transport_type: Optional[str] = None
    inventory: Optional[str] = None
    port_import: Optional[str] = None
    port_import_code: Optional[str] = None
    wunit: Optional[str] = None
    portcode: Optional[str] = None
    decln_ucr: Optional[str] = None
    interface: Optional[Interface] = None
    edi_cdec_itm_ai: Optional[EDICdecItmAI] = None
    customs_item: Optional[List[CustomsItem]] = None
    edi_cdec_itm: Optional[List[EDICdecItm]] = None

    def __post_init__(self):
        self.interface = Interface()
        self.consignor_address = []
        self.importer_address = []
        self.agent_address = []
        self.edi_cdec_itm_ai = EDICdecItmAI()
        self.customs_item  = []
        self.edi_cdec_itm = []

    def to_dict(self) -> dict:
        result: dict = {}
        result["customs_ref"] = from_union([from_str, from_none], self.customs_ref)
        result["mfrt-job-id"] = from_union([from_str, from_none], self.mfrt_job_id)
        result["consignor-code"] = from_union([from_str, from_none], self.consignor_code)
        result["importer-code"] = from_union([from_str, from_none], self.importer_code)
        result["agent-code"] = from_union([from_str, from_none], self.agent_code)
        result["consignor-name"] = from_union([from_str, from_none], self.consignor_name)
        result["_LIST_consignor-address_LIST"] = from_union([lambda x: from_list(from_str, x), from_none], self.consignor_address)
        result["consignor-county"] = from_union([from_str, from_none], self.consignor_county)
        result["consignor-country"] = from_union([from_str, from_none], self.consignor_country)
        result["enttype"] = from_union([from_str, from_none], self.enttype)
        result["importer-name"] = from_union([from_str, from_none], self.importer_name)
        result["_LIST_importer-address_LIST"] = from_union([lambda x: from_list(from_str, x), from_none], self.importer_address)
        result["importer-county"] = from_union([from_str, from_none], self.importer_county)
        result["importer-country"] = from_union([from_str, from_none], self.importer_country)
        result["importer-vatregn"] = from_union([from_str, from_none], self.importer_vatregn)
        result["agent-name"] = from_union([from_str, from_none], self.agent_name)
        result["_LIST_agent-address_LIST"] = from_union([lambda x: from_list(from_str, x), from_none], self.agent_address)
        result["agent-county"] = from_union([from_str, from_none], self.agent_county)
        result["agent-country"] = from_union([from_str, from_none], self.agent_country)
        result["agent-vatregn"] = from_union([from_str, from_none], self.agent_vatregn)
        result["agent-tel"] = from_union([from_str, from_none], self.agent_tel)
        result["pkgs"] = from_union([from_str, from_none], self.pkgs)
        result["gross_weight"] = from_union([from_str, from_none], self.gross_weight)
        result["port_loading"] = from_union([from_str, from_none], self.port_loading)
        result["country_dispatch"] = from_union([from_str, from_none], self.country_dispatch)
        result["transport_type"] = from_union([from_str, from_none], self.transport_type)
        result["inventory"] = from_union([from_str, from_none], self.inventory)
        result["port_import"] = from_union([from_str, from_none], self.port_import)
        result["port_import_code"] = from_union([from_str, from_none], self.port_import_code)
        result["wunit"] = from_union([from_str, from_none], self.wunit)
        result["portcode"] = from_union([from_str, from_none], self.portcode)
        result["decln_ucr"] = from_union([from_str, from_none], self.decln_ucr)
        result["INTERFACE"] = from_union([lambda x: to_class(Interface, x), from_none], self.interface)
        result["edi_cdec_itm_ai"] = from_union([lambda x: to_class(EDICdecItmAI, x), from_none], self.edi_cdec_itm_ai)
        result["_LIST_CUSTOMS-ITEM_LIST"] = from_union([lambda x: from_list(lambda x: to_class(CustomsItem, x), x), from_none], self.customs_item)
        result["_LIST_EDI_CDEC_ITM_LIST"] = from_union([lambda x: from_list(lambda x: to_class(EDICdecItm, x), x), from_none], self.edi_cdec_itm)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class EDICdec:
    tdr_own_ref_ent: Optional[str] = None
    ttr_own_ref_ent: Optional[str] = None
    declt_rep: Optional[str] = None
    disp_cntry: Optional[str] = None
    fir_dan: Optional[str] = None
    fir_dan_pfx: Optional[str] = None
    gds_locn_code: Optional[str] = None
    pla_ldg_code: Optional[str] = None
    tot_pkgs: Optional[str] = None
    trpt_cntry: Optional[str] = None
    trpt_id: Optional[str] = None
    trpt_mode_code: Optional[str] = None
    cnsge_city: Optional[str] = None
    cnsge_cntry: Optional[str] = None
    cnsge_name: Optional[str] = None
    cnsge_postcode: Optional[str] = None
    cnsge_street: Optional[str] = None
    cnsge_tid: Optional[str] = None
    cnsgr_city: Optional[str] = None
    cnsgr_cntry: Optional[str] = None
    cnsgr_name: Optional[str] = None
    cnsgr_postcode: Optional[str] = None
    cnsgr_street: Optional[str] = None
    cnsgr_tid: Optional[str] = None
    declt_city: Optional[str] = None
    declt_cntry: Optional[str] = None
    declt_name: Optional[str] = None
    declt_postcode: Optional[str] = None
    declt_street: Optional[str] = None
    declt_tid: Optional[str] = None
    intd_arr_dtm: Optional[str] = None
    inv_crrn: Optional[str] = None
    inv_tot_ac: Optional[str] = None
    interface: Optional[Interface] = None
    decln_ucr: Optional[str] = None
    farp_code: Optional[str] = None
    frgt_chge_ac: Optional[str] = None
    atrpt_cost_ac: Optional[str] = None
    frgt_chge_crrn: Optional[str] = None
    vat_adjt_ac: Optional[str] = None
    vat_adjt_crrn: Optional[str] = None
    decln_type: Optional[str] = None
    dest_cntry: Optional[str] = None
    gds_dep_dt: Optional[str] = None
    trpt_mode_inld: Optional[str] = None

    def to_dict(self) -> dict:
        result: dict = {}
        result["tdr_own_ref_ent"] = from_union([from_str, from_none], self.tdr_own_ref_ent)
        result["ttr_own_ref_ent"] = from_union([from_str, from_none], self.ttr_own_ref_ent)
        result["vat_adjt_ac"] = from_union([from_str, from_none], self.vat_adjt_ac)
        result["vat_adjt_crrn"] = from_union([from_str, from_none], self.vat_adjt_crrn)
        result["atrpt_cost_ac"] = from_union([from_str, from_none], self.atrpt_cost_ac)
        result["farp_code"] = from_union([from_str, from_none], self.farp_code)
        result["frgt_chge_ac"] = from_union([from_str, from_none], self.frgt_chge_ac)
        result["frgt_chge_crrn"] = from_union([from_str, from_none], self.frgt_chge_crrn)
        result["declt_rep"] = from_union([from_str, from_none], self.declt_rep)
        result["disp_cntry"] = from_union([from_str, from_none], self.disp_cntry)
        result["fir_dan"] = from_union([from_str, from_none], self.fir_dan)
        result["fir_dan_pfx"] = from_union([from_str, from_none], self.fir_dan_pfx)
        result["gds_locn_code"] = from_union([from_str, from_none], self.gds_locn_code)
        result["pla_ldg_code"] = from_union([from_str, from_none], self.pla_ldg_code)
        result["tot_pkgs"] = from_union([from_str, from_none], self.tot_pkgs)
        result["trpt_cntry"] = from_union([from_str, from_none], self.trpt_cntry)
        result["trpt_id"] = from_union([from_str, from_none], self.trpt_id)
        result["trpt_mode_code"] = from_union([from_str, from_none], self.trpt_mode_code)
        result["cnsge_city"] = from_union([from_str, from_none], self.cnsge_city)
        result["cnsge_cntry"] = from_union([from_str, from_none], self.cnsge_cntry)
        result["cnsge_name"] = from_union([from_str, from_none], self.cnsge_name)
        result["cnsge_postcode"] = from_union([from_str, from_none], self.cnsge_postcode)
        result["cnsge_street"] = from_union([from_str, from_none], self.cnsge_street)
        result["cnsge_tid"] = from_union([from_str, from_none], self.cnsge_tid)
        result["cnsgr_city"] = from_union([from_str, from_none], self.cnsgr_city)
        result["cnsgr_cntry"] = from_union([from_str, from_none], self.cnsgr_cntry)
        result["cnsgr_name"] = from_union([from_str, from_none], self.cnsgr_name)
        result["cnsgr_postcode"] = from_union([from_str, from_none], self.cnsgr_postcode)
        result["cnsgr_street"] = from_union([from_str, from_none], self.cnsgr_street)
        result["cnsgr_tid"] = from_union([from_str, from_none], self.cnsgr_tid)
        result["declt_city"] = from_union([from_str, from_none], self.declt_city)
        result["declt_cntry"] = from_union([from_str, from_none], self.declt_cntry)
        result["declt_name"] = from_union([from_str, from_none], self.declt_name)
        result["declt_postcode"] = from_union([from_str, from_none], self.declt_postcode)
        result["declt_street"] = from_union([from_str, from_none], self.declt_street)
        result["declt_tid"] = from_union([from_str, from_none], self.declt_tid)
        result["intd_arr_dtm"] = from_union([from_str, from_none], self.intd_arr_dtm)
        result["inv_crrn"] = from_union([from_str, from_none], self.inv_crrn)
        result["inv_tot_ac"] = from_union([from_str, from_none], self.inv_tot_ac)
        result["decln_ucr"] = from_union([from_str, from_none], self.decln_ucr)
        result["decln_type"] = from_union([from_str, from_none], self.decln_type)
        result["dest_cntry"] = from_union([from_str, from_none], self.dest_cntry)
        result["gds_dep_dt"] = from_union([from_str, from_none], self.gds_dep_dt)
        result["trpt_mode_inld"] = from_union([from_str, from_none], self.trpt_mode_inld)
        result["INTERFACE"] = from_union([lambda x: to_class(Interface, x), from_none], self.interface)
        return {k: v for k, v in result.items() if v is not None}
      
@dataclass
class NesItem:
    item_no: Optional[str] = None
    item_grs_mass: Optional[str] = None
    item_desc: Optional[str] = None
    edi_cdec_itm_ai: Optional[List[EDICdecItmAI]] = None
    edi_cdec_itm_cnt: Optional[List[EDICdecItmCnt]] = None
    edi_cdec_itm_pdc: Optional[List[EDICdecItmPdc]] = None
    edi_cdec_itm_pkg: Optional[List[EDICdecItmPkg]] = None

    def __post_init__(self):
        self.edi_cdec_itm_ai = []
        self.edi_cdec_itm_cnt = []
        self.edi_cdec_itm_pdc = []
        self.edi_cdec_itm_pkg = []

    def to_dict(self) -> dict:
        result: dict = {}
        result["item_no"] = from_union([from_str, from_none], self.item_no)
        result["item-grs-mass"] = from_union([from_str, from_none], self.item_grs_mass)
        result["item-desc"] = from_union([from_str, from_none], self.item_desc)
        result["_LIST_EDI_CDEC_ITM_AI_LIST"] = from_union([lambda x: from_list(lambda x: to_class(EDICdecItmAI, x), x), from_none], self.edi_cdec_itm_ai)
        result["_LIST_EDI_CDEC_ITM_CNT_LIST"] = from_union([lambda x: from_list(lambda x: to_class(EDICdecItmCnt, x), x), from_none], self.edi_cdec_itm_cnt)
        result["_LIST_EDI_CDEC_ITM_PDC_LIST"] = from_union([lambda x: from_list(lambda x: to_class(EDICdecItmPdc, x), x), from_none], self.edi_cdec_itm_pdc)
        result["_LIST_EDI_CDEC_ITM_PKG_LIST"] = from_union([lambda x: from_list(lambda x: to_class(EDICdecItmPkg, x), x), from_none], self.edi_cdec_itm_pkg)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class Nes:
    customs_ref: Optional[str] = None
    airwaybill_no: Optional[str] = None
    addr_consor_code: Optional[str] = None
    addr_consee_code: Optional[str] = None
    addr_consignee_name: Optional[str] = None
    addr_consignee_address: Optional[str] = None
    addr_consignee_county: Optional[str] = None
    addr_consignee_country: Optional[str] = None
    addr_consignor_name: Optional[str] = None
    addr_consignor_address: Optional[str] = None
    addr_consignor_county: Optional[str] = None
    addr_consignor_country: Optional[str] = None
    addr_declt_code: Optional[str] = None
    dest_cntry: Optional[str] = None
    gds_dep_dt: Optional[str] = None
    pla_ldg: Optional[str] = None
    stat_crrn: Optional[str] = None
    tdr_own_ref_ent: Optional[str] = None
    tot_pkgs: Optional[str] = None
    enttype: Optional[str] = None
    route_cntry: Optional[str] = None
    portcode: Optional[str] = None
    mfrt_job_id: Optional[str] = None
    trpt_id: Optional[str] = None
    trpt_mode_code: Optional[str] = None
    nes_item: Optional[List[NesItem]] = None
    edi_cdec_itm: Optional[List[EDICdecItm]] = None
    edi_cdec_itm_ai: Optional[EDICdecItmAI] = None
    edi_cdec_itm_doc: Optional[EDICdecItmDoc] = None
    
    def __post_init__(self):
        self.nes_item = []
        self.edi_cdec_itm = []
        self.edi_cdec_itm_ai = EDICdecItmAI()
        self.edi_cdec_itm_doc = EDICdecItmDoc()

    def to_dict(self) -> dict:
        result: dict = {}
        result["customs-ref"] = from_union([from_str, from_none], self.customs_ref)
        result["airwaybill-no"] = from_union([from_str, from_none], self.airwaybill_no)
        result["addr-consor-code"] = from_union([from_str, from_none], self.addr_consor_code)
        result["addr-consee-code"] = from_union([from_str, from_none], self.addr_consee_code)
        result["addr-consignee-name"] = from_union([from_str, from_none], self.addr_consignee_name)
        result["addr-consignee-address"] = from_union([from_str, from_none], self.addr_consignee_address)
        result["addr-consignee_county"] = from_union([from_str, from_none], self.addr_consignee_county)
        result["addr-consignee-country"] = from_union([from_str, from_none], self.addr_consignee_country)
        result["addr-consignor-name"] = from_union([from_str, from_none], self.addr_consignor_name)
        result["addr-consignor-address"] = from_union([from_str, from_none], self.addr_consignor_address)
        result["addr-consignor-county"] = from_union([from_str, from_none], self.addr_consignor_county)
        result["addr-consignor-country"] = from_union([from_str, from_none], self.addr_consignor_country)
        result["addr-declt-code"] = from_union([from_str, from_none], self.addr_declt_code)
        result["dest-cntry"] = from_union([from_str, from_none], self.dest_cntry)
        result["gds-dep-dt"] = from_union([from_str, from_none], self.gds_dep_dt)
        result["pla-ldg"] = from_union([from_str, from_none], self.pla_ldg)
        result["stat-crrn"] = from_union([from_str, from_none], self.stat_crrn)
        result["tdr-own-ref-ent"] = from_union([from_str, from_none], self.tdr_own_ref_ent)
        result["tot-pkgs"] = from_union([from_str, from_none], self.tot_pkgs)
        result["enttype"] = from_union([from_str, from_none], self.enttype)
        result["route-cntry"] = from_union([from_str, from_none], self.route_cntry)
        result["portcode"] = from_union([from_str, from_none], self.portcode)
        result["mfrt-job-id"] = from_union([from_str, from_none], self.mfrt_job_id)
        result["trpt-id"] = from_union([from_str, from_none], self.trpt_id)
        result["trpt-mode-code"] = from_union([from_str, from_none], self.trpt_mode_code)
        result["EDI_CDEC_ITM_AI"] = from_union([lambda x: to_class(EDICdecItmAI, x), from_none], self.edi_cdec_itm_ai)
        result["EDI_CDEC_ITM_DOC"] = from_union([lambda x: to_class(EDICdecItmDoc, x), from_none], self.edi_cdec_itm_doc)
        result["_LIST_NES-ITEM_LIST"] = from_union([lambda x: from_list(lambda x: to_class(NesItem, x), x), from_none], self.nes_item)
        result["_LIST_EDI_CDEC_ITM_LIST"] = from_union([lambda x: from_list(lambda x: to_class(EDICdecItm, x), x), from_none], self.edi_cdec_itm)
        return {k: v for k, v in result.items() if v is not None}


@dataclass
class MsediExports:
    context: Optional[MSEDIIMPORTSContext] = None
    nes: Optional[Nes] = None
    edi_cdec: Optional[EDICdec] = None

    def __post_init__(self):
        self.context = MSEDIIMPORTSContext()
        self.nes = Nes()
        self.edi_cdec = EDICdec()

    def to_dict(self) -> dict:
        result: dict = {}
        result["Context"] = from_union([lambda x: to_class(MSEDIIMPORTSContext, x), from_none], self.context)
        result["NES"] = from_union([lambda x: to_class(Nes, x), from_none], self.nes)
        result["EDI_CDEC"] = from_union([lambda x: to_class(EDICdec, x), from_none], self.edi_cdec)
        return {k: v for k, v in result.items() if v is not None}

@dataclass
class MsediImports:
    context: Optional[MSEDIIMPORTSContext] = None
    customs: Optional[Customs] = None
    edi_cdec: Optional[EDICdec] = None

    def __post_init__(self):
        self.context = MSEDIIMPORTSContext()
        self.customs = Customs()
        self.edi_cdec = EDICdec()

    def to_dict(self) -> dict:
        result: dict = {}
        result["Context"] = from_union([lambda x: to_class(MSEDIIMPORTSContext, x), from_none], self.context)
        result["CUSTOMS"] = from_union([lambda x: to_class(Customs, x), from_none], self.customs)
        result["EDI_CDEC"] = from_union([lambda x: to_class(EDICdec, x), from_none], self.edi_cdec)
        return {k: v for k, v in result.items() if v is not None}

@dataclass
class MFXml:
    isledi: Optional[Isledi] = None
    msedi_imports: Optional[MsediImports] = None
    msedi_exports: Optional[MsediExports] = None
    xml_type: str = None

    def __post_init__(self):
        self.isledi = Isledi()
        self.msedi_imports = MsediImports()
        self.msedi_exports = MsediExports()

    def to_dict(self) -> dict:
        result: dict = {}
        result["ISLEDI"] = from_union([lambda x: to_class(Isledi, x), from_none], self.isledi)
        if self.xml_type == 'Import':
            result["MSEDI-IMPORTS"] = from_union([lambda x: to_class(MsediImports, x), from_none], self.msedi_imports)
        elif self.xml_type == 'Export': 
            result["MSEDI-EXPORTS"] = from_union([lambda x: to_class(MsediExports, x), from_none], self.msedi_exports)
        return {k: v for k, v in result.items() if v is not None}

    def to_xml(self, pretty=True):

        def list_item_func(list):
            ltrim = list[6:]
            return ltrim[:-5]

        def stripper(data):
            new_data = {}
            for k, v in data.items():
                if k == 'INTERFACE':
                    new_data[k] = v
                else:
                    #if k !='INTERFACE':
                    if isinstance(v, dict):
                        v = stripper(v)
                    if isinstance(v, list):
                        new_list = []
                        for i in v: 
                            if isinstance(i, str):
                                new_list.append(i)
                            else:
                                new_list.append(stripper(i))
                        v=new_list
                    if not v in (u'', None, {}):
                        new_data[k] = v
                    #else:
                        #new_data[k] = v
            return new_data            

        mfLibDict = self.to_dict()
        #pprint.pprint(mfLibDict)
        cleanRes = stripper(mfLibDict)
        #print(cleanRes)
        xml = dicttoxml.dicttoxml(cleanRes,attr_type=False, item_func=list_item_func,custom_root='COMBINED')

         #while not cleanRes["isClean"]:
         #   cleanRes = remove_empty_keys(cleanRes["d"])
        
        #print(mfLibDictClean)
        #xml = dicttoxml.dicttoxml(self.to_dict(),attr_type=False, item_func=list_item_func,custom_root='COMBINED')
        
        #print(xml)
        #root = etree.fromstring(xml)
        #for element in root.xpath(".//*[not(node())]"):
        #    element.getparent().remove(element)

        #print(etree.tostring(root, pretty_print=True))
        #print(parseString(xml.decode("utf-8")).toprettyxml())
        cleanxml = re.sub('<_LIST_.*?_LIST>', '', xml.decode("utf-8"))
        cleanerxml = re.sub('</_LIST_.*?_LIST>', '', cleanxml)
        commentInsert = re.sub('<COMBINED>', '<COMBINED><!--JOB-->', cleanerxml)
        commentInsert2 = re.sub('</ISLEDI>', '</ISLEDI><!--ENTRY-->', commentInsert)
        
        
        finalxml = re.sub('<PostProcess>MultiShed-xml</PostProcess>', '<PostProcess FileName="#FILENAME#" OutputFolder="#MESSAGESERVERFILENAME#">MultiShed-xml</PostProcess>', commentInsert2)

        #removeEmptyLists = re.sub('<[a-zA-z_-]*?><[a-zA-z_-]*?>', '', finalxml)
        #print(removeEmptyLists)
        #result = re.search('<CUSTOMS>(.*)</CUSTOMS>', finalxml)
        #print(len(result.group(1)))
        #print(parseString(finalxml).toprettyxml(indent="    "))
        #if pretty:
        return parseString(finalxml).toprettyxml(indent="    ")
        ##return escape(parseString(finalxml).toprettyxml(indent="    "))       ##potential escape character fix

        #return finalxml