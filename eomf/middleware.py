from cStringIO import StringIO
import zipfile

class KMLMiddleware(object):
    """
    Middleware for serving KML data and optionally converting it to KMZ if the right extension is used.
    """
    def process_response(self, request, response):
        request_file = request.path.split("/")[-1]

        if request_file.lower().endswith(".kmz"):
            kmz = StringIO()
            f = zipfile.ZipFile(kmz, 'w', zipfile.ZIP_DEFLATED)
            save_file_name = request_file[:request_file.lower().rfind(".kmz")] # strips off the .kmz extension
            f.writestr('%s.kml' % save_file_name, response.content)
            f.close()
            response.content = kmz.getvalue()
            kmz.close()
            response['Content-Type']        = 'application/vnd.google-earth.kmz'
            response['Content-Disposition'] = 'attachment; filename=%s.kmz' % save_file_name
            response['Content-Length']      = str(len(response.content))
        if request_file.lower().endswith(".kml"):
            save_file_name = request_file[:request_file.lower().rfind(".kml")] # strips off the .kmz extension
            response['Content-Type']        = 'application/vnd.google-earth.kml+xml'
            response['Content-Disposition'] = 'attachment; filename=%s.kml' % save_file_name
            response['Content-Length']      = str(len(response.content))
            
        return response
