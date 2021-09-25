from scrapy.pipelines.images import ImagesPipeline

class CustomProductsImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item):
        imagen = item['images'] + '.jpeg'
        return imagen