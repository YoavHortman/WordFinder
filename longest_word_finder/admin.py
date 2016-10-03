from django.contrib import admin
import longest_word_finder.models

admin.site.register(longest_word_finder.models.Action)
admin.site.register(longest_word_finder.models.Rank)
admin.site.register(longest_word_finder.models.Word)
admin.site.register(longest_word_finder.models.ActionType)
admin.site.register(longest_word_finder.models.Description)
