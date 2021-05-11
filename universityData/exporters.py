from scrapy.exporters import JsonItemExporter


class Utf8JsonItemExporter(JsonItemExporter):

    def __init__(self, file, **kwargs):
        super(Utf8JsonItemExporter, self).__init__(
            file, ensure_ascii=False, **kwargs)