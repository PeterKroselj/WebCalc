#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        params = {"sporocilo": self.request.get("arg1")}
        return self.render_template("home.html", params=params)

    def post(self):
        arg1str = self.request.get("arg1")
        oprstr = self.request.get("opr")
        arg2str = self.request.get("arg2")

        arg1 = float(arg1str)
        arg2 = float(arg2str)

        if oprstr == '+':
            res = arg1 + arg2
            resstr = str(res)
        elif oprstr == '-':
            res = arg1 - arg2
            resstr = str(res)
        elif oprstr == '*':
            res = arg1 * arg2
            resstr = str(res)
        elif oprstr == '/':
            if arg2 <> 0:
                res = arg1 / arg2
                resstr = str(res)
            else:
                resstr = "Error"
        elif oprstr == '**':
            res = arg1 ** arg2
            resstr = str(res)
        else:
            resstr = "Error"


        rezultat = arg1str + " " + oprstr + " " + arg2str + " = " + resstr
        params = {"sporocilo": rezultat}
        return self.render_template("home.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
