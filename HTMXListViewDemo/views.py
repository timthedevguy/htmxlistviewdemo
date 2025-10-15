from urllib.parse import urlencode

from django.core.exceptions import FieldError
from django.views.generic import ListView

from .utils import build_filter_dict, build_query_str, build_filters_template_dict


class HtmxListView(ListView):
    target_id = ""

    def setup(self, request, *args, **kwargs):
        super(HtmxListView, self).setup(request, *args, **kwargs)
        self.filter = build_filter_dict(request.GET)
        self.query = build_query_str(request.GET)
        self.filter_query = self.query

        if "order_by" in request.GET:
            self.order_by = request.GET.get('order_by')

        if not self.order_by:
            self.order_by = "pk"

        self.query += f"&order_by={self.order_by}"

    def get_queryset(self):
        qs = super(HtmxListView, self).get_queryset()
        if hasattr(self, 'filter') and self.filter:
            qs = qs.filter(**self.filter)
        if hasattr(self, 'order_by') and self.order_by:
            try:
                qs = qs.order_by(self.order_by)
            except FieldError:
                # Most likely a @property, try to sort a different way
                # Experimental, sometimes works, sometimes not
                sort_key = self.order_by
                reversed = False
                if sort_key.startswith('-'):
                    reversed = True
                    sort_key = sort_key[1:]

                qs = sorted(qs.order_by("pk"), key=lambda obj: getattr(obj, sort_key, None), reverse=reversed)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_params = {p: v for p, v in self.request.GET.items() if p != 'page'}
        context["query_params"] = urlencode(query_params, doseq=True)

        if hasattr(self, 'paginate_by') and self.paginate_by:
            if not hasattr(self, 'elided_each_side'):
                self.elided_each_side = 1

            if not hasattr(self, 'elided_ends'):
                self.elided_ends = 1

            context["page_range"] = context["paginator"].get_elided_page_range(
                number=context["page_obj"].number, on_each_side=self.elided_each_side, on_ends=self.elided_ends
            )
            context["paginator"].allow_empty_first_page = True

        context["order_by"] = self.order_by
        context["path"] = self.request.path
        context["target_id"] = self.target_id
        context["query"] = self.query
        context["filter_query"] = self.filter_query
        context["filters"] = build_filters_template_dict(self.filter)

        return context
