from flask import Blueprint, request, jsonify
import os
import math

from flask.helpers import send_from_directory


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)


api_images = Blueprint('api_images', __name__)


@api_images.route("/")
def bienvenida():
    return "Bienvenido al API"


@api_images.route("/tiles/<lat>/<lon>/<zoom>", methods=['GET'])
def getTile(lat, lon, zoom):
    if request.method == "GET":

        if int(zoom) >= 7 and int(zoom) <= 12:
            refTile = deg2num(float(lat), float(lon), int(zoom))
            xtile = refTile[0]
            ytile = refTile[1]
            if int(zoom) == 7:
                ytile_tsm = (127 - ytile)
            elif int(zoom) == 8:
                ytile_tsm = (255 - ytile)
            elif int(zoom) == 9:
                ytile_tsm = (511 - ytile)
            elif int(zoom) == 10:
                ytile_tsm = (1023 - ytile)
            elif int(zoom) == 11:
                ytile_tsm = (2047 - ytile)
            elif int(zoom) == 12:
                ytile_tsm = (4095 - ytile)

            filename = str(ytile_tsm) + ".png"
            pathTile = os.getcwd() + "/tiles/" + str(zoom) + "/" + str(xtile) + "/"

            if os.path.exists(pathTile + filename):
                return send_from_directory(pathTile, filename, as_attachment=False), 200
            else:
                return jsonify({'msg': 'No existe el Tile'}), 500
        else:
            return jsonify({'msg': 'El Zoom valido es entre 7 y 12'}), 500
    else:
        return jsonify({'msg': 'Internal server error'}), 500


@api_images.route("/image/<yt>/<xt>/<zoom>", methods=['GET'])
def getImage(yt, xt, zoom):
    if request.method == "GET":
        if int(zoom) >= 7 and int(zoom) <= 12:
            xtile = int(xt)
            ytile = int(yt)
            if int(zoom) == 7:
                ytile_tsm = (127 - ytile)
            elif int(zoom) == 8:
                ytile_tsm = (255 - ytile)
            elif int(zoom) == 9:
                ytile_tsm = (511 - ytile)
            elif int(zoom) == 10:
                ytile_tsm = (1023 - ytile)
            elif int(zoom) == 11:
                ytile_tsm = (2047 - ytile)
            elif int(zoom) == 12:
                ytile_tsm = (4095 - ytile)

            filename = str(ytile_tsm) + ".png"
            pathTile = os.getcwd() + "/tiles/" + str(zoom) + "/" + str(xtile) + "/"

            if os.path.exists(pathTile + filename):
                return send_from_directory(pathTile, filename, as_attachment=False), 200
            else:
                return jsonify({'msg': 'No existe el Tile'}), 500
        else:
            return jsonify({'msg': 'El Zoom valido es entre 7 y 12'}), 500
    else:
        return jsonify({'msg': 'Internal server error'}), 500


@api_images.route("/tiles", methods=['POST'])
def postTile():
    if request.method == "POST":

        if request.json.get("longitud") and request.json.get("latitud") and request.json.get("zoom"):
            if type(request.json['zoom']) == str:
                latitud = float(request.json['latitud'])
            else:
                latitud = request.json['latitud']

            if type(request.json['zoom']) == str:
                longitud = float(request.json['longitud'])
            else:
                longitud = request.json['longitud']

            if type(request.json['zoom']) == str:
                zoom = int(request.json['zoom'])
            else:
                zoom = request.json['zoom']

            if zoom >= 7 and zoom <= 12:
                refTile = deg2num(latitud, longitud, zoom)
                xtile = refTile[0]
                ytile = refTile[1]
                if zoom == 7:
                    ytile_tsm = (127 - ytile)
                elif zoom == 8:
                    ytile_tsm = (255 - ytile)
                elif zoom == 9:
                    ytile_tsm = (511 - ytile)
                elif zoom == 10:
                    ytile_tsm = (1023 - ytile)
                elif zoom == 11:
                    ytile_tsm = (2047 - ytile)
                elif zoom == 12:
                    ytile_tsm = (4095 - ytile)

                filename = str(ytile_tsm) + ".png"
                pathTile = os.getcwd() + "/tiles/" + str(zoom) + "/" + str(xtile) + "/"

                if os.path.exists(pathTile + filename):
                    return send_from_directory(pathTile, filename, as_attachment=False), 200
                else:
                    return jsonify({'msg': 'No existe el Tile'}), 500
            else:
                return jsonify({'msg': 'El Zoom valido es entre 7 y 12'}), 500
        else:
            return jsonify({'msg': 'Internal server error'}), 500
