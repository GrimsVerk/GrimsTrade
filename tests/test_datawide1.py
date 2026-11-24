"""The data-wide-1 loaders parse what the sources publish and date it no earlier than public."""
# ruff: noqa: E501  (literal sample rows from the sources, kept verbatim)

from __future__ import annotations

import importlib
import json
import math
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _dw() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("datawide1")
    finally:
        sys.path.remove(str(LIB))


USGS = """time,latitude,longitude,depth,mag,magType,nst,gap,dmin,rms,net,id,updated,place,type,horizontalError,depthError,magError,magNst,status,locationSource,magSource
2011-03-11T05:46:24.120Z,38.297,142.373,29,9.1,mww,541,9.5,,1.16,us,official20110311054624120_30,2022-04-27T18:00:50.123Z,"2011 Great Tohoku Earthquake, Japan",earthquake,,,,,reviewed,us,us
2011-03-11T06:15:40.280Z,36.281,141.111,42.6,7.9,mww,,,,1.1,us,usp000hvp2,2022-04-27T18:01:00.000Z,"near the east coast of Honshu, Japan",earthquake,,,,,reviewed,us,us
2011-03-11T23:59:00.000Z,10,10,10,6.0,mb,,,,,us,x1,2020-01-01T00:00:00.000Z,"somewhere",quarry blast,,,,,reviewed,us,us
2011-03-12T01:47:15.660Z,37.578,141.588,25,,mb,,,,,us,x2,2020-01-01T00:00:00.000Z,"no magnitude",earthquake,,,,,reviewed,us,us
2011-03-12T01:47:16.000Z,37.5,141.5,,6.4,mw,,,,,us,x3,2020-01-01T00:00:00.000Z,"no depth",earthquake,,,,,reviewed,us,us
"""


def test_usgs_keeps_earthquakes_with_a_magnitude() -> None:
    qs = _dw().parse_usgs_csv(USGS)
    assert [q.id for q in qs] == ["official20110311054624120_30", "usp000hvp2", "x3"]
    q = qs[0]
    assert q.time == datetime(2011, 3, 11, 5, 46, 24, 120000, tzinfo=UTC)
    assert q.mag == 9.1 and q.mag_type == "mww" and q.lat == 38.297
    assert q.place == "2011 Great Tohoku Earthquake, Japan"
    assert math.isnan(qs[2].depth_km)


def test_usgs_merge_keeps_latest_revision_and_orders_by_time() -> None:
    dw = _dw()
    a = dw.parse_usgs_csv(USGS)
    revised = dw.Quake(**{**a[1].__dict__, "mag": 7.7, "updated": a[1].updated + timedelta(1)})
    merged = dw.merge_quakes([a, [revised], a[:1]])
    assert len(merged) == 3
    assert merged[1].mag == 7.7  # the later revision wins, whichever file it came from
    assert [q.time for q in merged] == sorted(q.time for q in merged)


def test_daily_max_magnitude_groups_by_utc_day() -> None:
    dw = _dw()
    qs = dw.parse_usgs_csv(USGS)
    assert dw.daily_max_magnitude(qs, 6.0) == {date(2011, 3, 11): 9.1, date(2011, 3, 12): 6.4}
    assert dw.daily_max_magnitude(qs, 8.0) == {date(2011, 3, 11): 9.1}


GPR_HEAD = ["DAY", "N10D", "GPRD", "GPRD_ACT", "GPRD_THREAT", "date", "GPRD_MA30", "event"]


def test_gpr_rows_by_column_name_any_order() -> None:
    rows = [
        GPR_HEAD,
        ["19850102", 220.0, 296.4, 300.1, 150.2, 31049.0, 1.0, "x"],
        [19850101.0, 216.0, 230.04, 275.2, 153.03, 31048.0, 1.0, ""],
        ["", "", "", "", "", "", "", "trailing label row"],
    ]
    got = _dw().parse_gpr_rows(rows)
    assert [g.day for g in got] == [date(1985, 1, 1), date(1985, 1, 2)]
    assert got[0].gprd == 230.04 and got[0].act == 275.2 and got[0].threat == 153.03
    assert got[0].articles == 216


def test_gpr_available_on_is_a_wednesday_nine_to_fifteen_days_later() -> None:
    dw = _dw()
    assert dw.gpr_available_on(date(2026, 11, 16)) == date(2026, 11, 25)  # Monday -> +9
    d = date(2024, 1, 1)
    for k in range(400):
        day = d + timedelta(k)
        a = dw.gpr_available_on(day)
        assert a.weekday() == 2
        assert 9 <= (a - day).days <= 15


FDIC = {
    "meta": {"total": 2},
    "data": [
        {
            "data": {
                "QBFDEP": 68773, "COST": None, "QBFASSET": 72947, "PSTALP": "KS",
                "FAILDATE": "7/17/2026", "CERT": 25744, "RESTYPE": "FAILURE", "SAVR": "DIF",
                "RESTYPE1": "PA", "NAME": "SMALL BANK B",
            }
        },
        {
            "data": {
                "QBFDEP": 1064, "COST": 5, "QBFASSET": 1435, "PSTALP": "PA",
                "FAILDATE": "4/19/1934", "CERT": None, "RESTYPE": "FAILURE", "SAVR": "FDIC",
                "RESTYPE1": "PO", "NAME": "OLD BANK A",
            }
        },
    ],
}  # fmt: skip


def test_fdic_failures_parse_and_sort() -> None:
    dw = _dw()
    fs = dw.parse_fdic_failures(json.dumps(FDIC))
    assert [f.day for f in fs] == [date(1934, 4, 19), date(2026, 7, 17)]
    assert fs[0].cert is None and fs[0].cost_k == 5.0 and fs[0].resolution == "PO"
    assert fs[1].cert == 25744 and math.isnan(fs[1].cost_k) and fs[1].assets_k == 72947.0
    assert dw.failure_available_on(date(2026, 7, 17)) == date(2026, 7, 18)


MOF_LINES = [
    "財務省,,,,,,,,,,,,,,",
    "Ministry of Finance,,,,,,,,,,,,,,",
    "(amount:100 million Yen),,,,,,,,,,,,,,",
    "実施年月日,,,Intervention Date,,,,,,,,,,,",
    "年,月,日,Year,Month,Day,金額(amount),売買通貨,Currency pairs,,,,,,",
    "平成3年,5月,13日,1991,May,13,139,米ドル売り・日本円買い,the US dollar (sold) the Japanese yen (bought),,,,,,",
    ",6月,10日,,Jun,10,211,米ドル売り・日本円買い,the US dollar (sold) the Japanese yen (bought),,,,,,",
    ",,13日,,,13,213,米ドル売り・日本円買い,the US dollar (sold) the Japanese yen (bought),,,,,,",
    "平成3年4〜6月期計,,,April - June 1991,,,563,,,,,,,,",
    "平成3年,8月,19日,1991,Aug,19,139,米ドル売り・独マルク買い,the US dollar (sold) the German mark (bought),,,,,,",
    "平成3年7〜9月期計,,,July - September 1991,,,139,,,,,,,,",
    '令和4年,10月,21日,2022,Oct,21,"56,202",米ドル売り・日本円買い,the US dollar (sold) the Japanese yen (bought),,,,,,',
    '平成15年,10月,1日,2003,Oct,1,"2,998",米ドル買い・日本円売り,the US dollar (bought) the Japanese yen (sold),,,,,,',
    '平成13年10〜12月期計,,,October - December 200１,,,0,,,,,,,,',
    '"(note2) As the figures in each days are rounded off, they do not necessarily add up.",,,,,,,,,,,,,,',
]  # fmt: skip
MOF = ("\r\n".join(MOF_LINES) + "\r\n").encode("shift_jis")


def test_mof_daily_rows_carry_year_and_month_down() -> None:
    ops = _dw().parse_mof_csv(MOF)
    assert [o.day for o in ops] == [
        date(1991, 5, 13),
        date(1991, 6, 10),
        date(1991, 6, 13),
        date(1991, 8, 19),
        date(2022, 10, 21),
        date(2003, 10, 1),
    ]
    assert [o.amount for o in ops] == [139, 211, 213, 139, 56202, 2998]
    assert [o.yen_sign for o in ops] == [1, 1, 1, 0, 1, -1]


def test_mof_quarter_totals_and_monthly_sums() -> None:
    dw = _dw()
    q = dw.mof_quarter_totals(MOF)
    assert q == {(1991, 2): 563, (1991, 3): 139, (2001, 4): 0}  # full-width digit normalised
    ops = dw.parse_mof_csv(MOF)
    assert sum(o.amount for o in ops if o.day.year == 1991 and o.day.month <= 6) == q[(1991, 2)]
    m = dw.monthly_totals(ops)
    assert m[(1991, 6)] == 424 and m[(1991, 8)] == 0 and m[(2003, 10)] == -2998
    assert dw.monthly_totals(ops, signed=False)[(1991, 8)] == 139


def test_mof_availability_never_before_publication() -> None:
    dw = _dw()
    assert dw.mof_month_available_on(2024, 4) == date(2024, 5, 1)
    assert dw.mof_month_available_on(2024, 12) == date(2025, 1, 1)
    assert dw.mof_daily_available_on(date(2024, 4, 29)) == date(2024, 6, 30) + timedelta(45)
    assert dw.mof_daily_available_on(date(2024, 12, 31)) == date(2024, 12, 31) + timedelta(45)


def test_snapshot_picks_latest_dated_folder(tmp_path: Path) -> None:
    dw = _dw()
    for d in ("2026-11-01", "2026-11-19", "2026-11-05"):
        (tmp_path / "data-wide-1" / "usgs" / d).mkdir(parents=True)
    assert dw.snapshot("usgs", tmp_path).name == "2026-11-19"
