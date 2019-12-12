from flask import (flash, jsonify, redirect, render_template, Response,
                   request, url_for)
from flask.views import MethodView


def response(message: str, status_code: int = 200,
             category: str = None, payload: dict = None):
    if request.is_json:
        if payload is not None:
            # return payload
            return {
                "payload": payload,
                "status_code": status_code
            }
        else:
            return {
                "message": message,
                "status_code": status_code
            }
    if category is None:
        category = "success"
        if status_code >= 500:
            category = "danger"
        elif status_code >= 400:
            category = "warning"
    flash("%s|%s" % (message, category), "notification")
    return {}


class AppRouteView(MethodView):
    headers = ["application/json", "text/html"]
    redirect_to = None
    route = None
    redirect_args = {}

    def get_template_name(self):
        # Overrideable
        return self.template_name

    def render_template(self, **context):
        return render_template(self.get_template_name(), **context)

    def before_request(self, *args, **kwargs):
        # Method is run regardless of HTTP method
        # Override
        pass

    def after_request(self, *args, **kwargs):
        # Method is run regardless of HTTP method
        # Override
        pass

    # GET requests {{{

    def populate(self, *args, **kwargs):
        # Override
        return {}

    def get_json(self, *args, **kwargs):
        values = self.populate(*args, **kwargs)
        if isinstance(values, Response):
            return values
        return jsonify(values), values.get("status_code", 200)

    def get_html(self, *args, **kwargs):
        return self.render_template(**self.populate(*args, **kwargs))

    # }}}

    # POST requests {{{
    # All HTTP POST requests should redirect to avoid refresh-duplication, so
    # do not overwrite post_html without a redirect

    def handle_post(self, values, *args, **kwargs) -> dict:
        """
        Must return a dict.
        Dict Formats:
        {
            "payload": <JSON serializable content>[,
            "status_code": <HTTP status number>]
        }
        {
            "message": "one-liner for quick output"[,
            "status_code": <HTTP status number>]
        }
        """
        raise NotImplementedError()

    def post_json(self, *args, **kwargs):
        values = request.json
        result = self.handle_post(values, *args, **kwargs)
        if isinstance(result, Response):
            return result
        if "payload" in result:
            return jsonify(result["payload"]), result.get("status_code", 200)
        return (jsonify({"message": result.get("message", "no output")}),
                result.get("status_code", 200))

    def post_html(self, *args, **kwargs):
        values = request.form
        result = self.handle_post(values, *args, **kwargs)
        if isinstance(result, Response):
            return result
        if self.redirect_to is not None:
            return redirect(url_for(self.redirect_to, **self.redirect_args))
        return redirect(url_for(request.url_rule.rule, **self.redirect_args))

    # }}}

    # PUT requests {{{
    # All HTTP PUT requests should redirect to avoid refresh-duplication, so
    # do not overwrite post_html without a redirect

    def handle_put(self, values, *args, **kwargs) -> dict:
        """
        Must return a dict.
        Dict Formats:
        {
            "payload": <JSON serializable content>[,
            "status_code": <HTTP status number>]
        }
        {
            "message": "one-liner for quick output"[,
            "status_code": <HTTP status number>]
        }
        """
        raise NotImplementedError()

    def put_json(self, *args, **kwargs):
        values = request.json
        result = self.handle_put(values, *args, **kwargs)
        if isinstance(result, Response):
            return result
        if "payload" in result:
            return jsonify(result["payload"]), result.get("status_code", 200)
        return (jsonify({"message": result.get("message", "no output")}),
                result.get("status_code", 200))

    def put_html(self, *args, **kwargs):
        values = request.form
        result = self.handle_put(values, *args, **kwargs)
        if isinstance(result, Response):
            return result
        if self.redirect_to is not None:
            return redirect(url_for(self.redirect_to, **self.redirect_args))
        return redirect(url_for(request.url_rule.rule, **self.redirect_args))

    # }}}

    # PATCH requests {{{
    # All HTTP PATCH requests should redirect to avoid refresh-duplication, so
    # do not overwrite post_html without a redirect

    def handle_patch(self, values, *args, **kwargs) -> dict:
        """
        Must return a dict.
        Dict Formats:
        {
            "payload": <JSON serializable content>[,
            "status_code": <HTTP status number>]
        }
        {
            "message": "one-liner for quick output"[,
            "status_code": <HTTP status number>]
        }
        """
        raise NotImplementedError()

    def patch_json(self, *args, **kwargs):
        values = request.json
        result = self.handle_patch(values, *args, **kwargs)
        if isinstance(result, Response):
            return result
        if "payload" in result:
            return jsonify(result["payload"]), result.get("status_code", 200)
        return (jsonify({"message": result.get("message", "no output")}),
                result.get("status_code", 200))

    def patch_html(self, *args, **kwargs):
        values = request.form
        result = self.handle_patch(values, *args, **kwargs)
        if isinstance(result, Response):
            return result
        if self.redirect_to is not None:
            return redirect(url_for(self.redirect_to, **self.redirect_args))
        return redirect(url_for(request.url_rule.rule, **self.redirect_args))

    # }}}

    # DELETE requests {{{
    # All HTTP DELETE requests should redirect to avoid refresh-duplication, so
    # do not overwrite post_html without a redirect

    def handle_delete(self, values, *args, **kwargs) -> dict:
        """
        Must return a dict.
        Dict Formats:
        {
            "payload": <JSON serializable content>[,
            "status_code": <HTTP status number>]
        }
        {
            "message": "one-liner for quick outdelete"[,
            "status_code": <HTTP status number>]
        }
        """
        raise NotImplementedError()

    def delete_json(self, *args, **kwargs):
        values = request.json
        result = self.handle_delete(values, *args, **kwargs)
        if isinstance(result, Response):
            return result
        if "payload" in result:
            return jsonify(result["payload"]), result.get("status_code", 200)
        return (jsonify({"message": result.get("message", "no outdelete")}),
                result.get("status_code", 200))

    def delete_html(self, *args, **kwargs):
        values = request.form
        result = self.handle_delete(values, *args, **kwargs)
        if isinstance(result, Response):
            return result
        if self.redirect_to is not None:
            return redirect(url_for(self.redirect_to, **self.redirect_args))
        return redirect(url_for(request.url_rule.rule, **self.redirect_args))

    # }}}

    # MethodView overrides {{{

    def get(self, *args, **kwargs):
        self.before_request(*args, **kwargs)
        if request.is_json:
            result = self.get_json(*args, **kwargs)
        else:
            result = self.get_html(*args, **kwargs)
        self.after_request(*args, **kwargs)
        return result

    def post(self, *args, **kwargs):
        self.before_request(*args, **kwargs)
        if request.is_json:
            result = self.post_json(*args, **kwargs)
        else:
            result = self.post_html(*args, **kwargs)
        self.after_request(*args, **kwargs)
        return result

    def put(self, *args, **kwargs):
        self.before_request(*args, **kwargs)
        if request.is_json:
            result = self.put_json(*args, **kwargs)
        else:
            result = self.put_html(*args, **kwargs)
        self.after_request(*args, **kwargs)
        return result

    def patch(self, *args, **kwargs):
        self.before_request(*args, **kwargs)
        if request.is_json:
            result = self.patch_json(*args, **kwargs)
        else:
            result = self.patch_html(*args, **kwargs)
        self.after_request(*args, **kwargs)
        return result

    def delete(self, *args, **kwargs):
        self.before_request(*args, **kwargs)
        if request.is_json:
            result = self.delete_json(*args, **kwargs)
        else:
            result = self.delete_html(*args, **kwargs)
        self.after_request(*args, **kwargs)
        return result

    # }}}
