menu = [{'title': "FFFFFFFF", 'url_name': 'about'},
        {'title': "retetertert", 'url_name': 'login'},
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        #games = Game.objects.all()

        #context['menu'] = menu


        #context['games'] = games
        #if 'game_selected' not in context:
        #    context['game_selected'] = 0
        return context
