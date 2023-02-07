import rasterio
import scipy.interpolate as spip


def get_get_alt(dem_name):
    dem = rasterio.open(dem_name)
    band = dem.read(1)

    def get_alt(lon, lat):
        r, c = dem.index(lon, lat)
        x, y = dem.xy(r, c)
        dx, dy = dem.res[0], dem.res[1]
        X = [x - dx, x, x + dx]
        Y = [y + dy, y, y - dy]
        Z = band[r - 1 : r + 2, c - 1 : c + 2]
        return spip.interp2d(X, Y, Z)(lon, lat)[0]

    return get_alt


def get_czml_header(name):
    return {"id": "document", "name": name, "version": "1.0"}


def get_czml_body(aid, name, epoch, flat_poss_list, box=None, ellipsoid=None):
    body = {
        "id": aid,
        "name": name,
        "position": {
            "epoch": epoch.strftime("%Y-%m-%dT%H:%M:%S+09"),
            "cartographicDegrees": flat_poss_list,
        },
        "orientation": {"velocityReference": "%s#position" % aid},
        "forwardExtrapolationType": "None",
        "backwardExtrapolationType": "None",
    }
    if box:
        body["box"] = box
    if ellipsoid:
        body["ellipsoid"] = ellipsoid
    return body
