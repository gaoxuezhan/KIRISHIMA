from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware


class FakeUserAgentErrorRetryMiddleware(RetryMiddleware):
    def process_request(self, request, spider):
        print("hello,request")
        return None

    def process_response(self, request, response, spider):
        print("hello,response")
        return self._retry(self, request, response, spider)

    def process_exception(self, request, exception, spider):
        return self._retry(request, exception, spider)
