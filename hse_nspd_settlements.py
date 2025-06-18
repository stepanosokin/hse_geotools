from osgeo import ogr
import requests
import os, json
from hse_general import smart_http_request


def download_nspd_settlements(s: requests.Session, tiles_gpkg='tiles.gpkg', tiles_layer='kaluga', width=512, height=512, i_from=0, i_to=512, j_from=0, j_to=512, pixel_step=3):    
    current_dir = os.getcwd()
    tiles_gpkg_fullpath = os.path.join(current_dir, tiles_gpkg)
    if os.path.exists(tiles_gpkg_fullpath):
        geojson_result = {
            "type": "FeatureCollection",
            "features": []
        }
        driver = ogr.GetDriverByName('GPKG')
        ds = driver.Open(tiles_gpkg_fullpath)
        layer = ds.GetLayer(tiles_layer)
        if layer:
            url = "https://nspd.gov.ru/api/aeggis/v3/36281/wms"
            params = {
                "REQUEST": "GetFeatureInfo",
                "SERVICE":"WMS",
                "VERSION": "1.3.0",
                "FORMAT": 'image/png',
                "STYLES": "",
                "TRANSPARENT": "true",
                "LAYERS": "36281",
                "RANDOM": "0.4158997836664142",
                "INFO_FORMAT": "application/json",
                "FEATURE_COUNT": "10",
                "I": "0",
                "J": "0",
                "WIDTH": str(width),
                "HEIGHT": str(height),
                "CRS": "EPSG:3857",
                "BBOX": "7592337.145509988,8000941.147561606,7670608.662474008,8079212.664525626",
                "QUERY_LAYERS": "36281"
                }
            pass
            for grid_feature in layer:
                extent = grid_feature.geometry().GetEnvelope()
                xmin, xmax, ymin, ymax = extent
                headers = {
                    "Referer": f"https://nspd.gov.ru/map?thematic=Default&zoom=14.087600258143208&coordinate_x={str((xmin + xmax) / 2)}&coordinate_y={str((ymin + ymax) / 2)}&theme_id=1&is_copy_url=true&active_layers=36281"
                    }
                params["BBOX"] = f"{xmin},{ymin},{xmax},{ymax}"
                for i in range(i_from, i_to + 1, pixel_step):
                    params["I"] = str(i)
                    for j in range(j_from, j_to + 1, pixel_step):
                        params["J"] = str(j)                        
                        status, result = smart_http_request(s, url=url, params=params, headers=headers)
                        if status == 200:
                            jdata = result.json()
                            # geojson_result["features"].extend(jdata["features"])
                            for feature in jdata["features"]:
                                # if feature["properties"]["options"]["guid"] not in [x["properties"]["options"]["guid"] for x in geojson_result.get("features")]:
                                #     geojson_result["features"].append(feature)
                                if feature["properties"]["options"]["guid"] not in [x["properties"]["guid"] for x in geojson_result.get("features")]:
                                    for k, v in feature["properties"]["options"].items():
                                        feature["properties"][k] = v
                                    feature["properties"].pop('options', None)
                                    geojson_result["features"].append(feature)
                pass
            geojson_result_path = os.path.join(current_dir, 'results', f"{tiles_layer}.json")
            with open(geojson_result_path, 'w', encoding='utf-8') as of:
                json.dump(geojson_result, of, ensure_ascii=False)
                return True
        pass
    
    return False


if __name__ == '__main__':
    # with requests.Session() as s:
    #     s.verify = False
    #     download_nspd_settlements(s, tiles_gpkg='tiles.gpkg', tiles_layer='kaluga', width=128, height=128, i_from=0, i_to=128, j_from=0, j_to=128, pixel_step=3)
    with requests.Session() as ss:
        download_nspd_settlements(ss, tiles_gpkg='tiles.gpkg', tiles_layer='lipetskaya', width=128, height=128, i_from=0, i_to=128, j_from=0, j_to=128, pixel_step=3)
    with requests.Session() as ss:
        download_nspd_settlements(ss, tiles_gpkg='tiles.gpkg', tiles_layer='volgogradskaya', width=128, height=128, i_from=0, i_to=128, j_from=0, j_to=128, pixel_step=3)
    with requests.Session() as ss:
        download_nspd_settlements(ss, tiles_gpkg='tiles.gpkg', tiles_layer='rostovskaya', width=128, height=128, i_from=0, i_to=128, j_from=0, j_to=128, pixel_step=3)
    with requests.Session() as ss:
        download_nspd_settlements(ss, tiles_gpkg='tiles.gpkg', tiles_layer='stavropolskiy', width=128, height=128, i_from=0, i_to=128, j_from=0, j_to=128, pixel_step=3)
    with requests.Session() as ss:
        download_nspd_settlements(ss, tiles_gpkg='tiles.gpkg', tiles_layer='krasnodarskiy', width=128, height=128, i_from=0, i_to=128, j_from=0, j_to=128, pixel_step=3)
    with requests.Session() as ss:
        download_nspd_settlements(ss, tiles_gpkg='tiles.gpkg', tiles_layer='tatarstan', width=128, height=128, i_from=0, i_to=128, j_from=0, j_to=128, pixel_step=3)
        