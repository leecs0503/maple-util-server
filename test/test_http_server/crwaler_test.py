from api_server.http_server.crwaler import Crwaler
from api_server.http_server.item_info import ItemInfo
import json
from pathlib import Path

TEST_DATA_NUM = 3

def _load_test_datas():
    test_data_dir = Path(__file__).parent / "views"
    test_datas = []
    expected_results = []
    for name in range(0, TEST_DATA_NUM):
        path = str(test_data_dir / f"{name + 1}.txt")
        with open(path) as f:
            test_datas.append(f.read())
        path = str(test_data_dir / f"{name + 1}_result.txt")
        with open(path) as f:
            x = json.loads(f.read())
            print(x)
            expected_results.append(
                ItemInfo(**x)
            )
    return test_datas, expected_results

def test_item_info_of():
    test_datas, expected_results = _load_test_datas()
    crwaler = Crwaler()
    for test_count, test_data in enumerate(test_datas):
        result = crwaler._item_info_of(test_data)
        assert expected_results[test_count] == result