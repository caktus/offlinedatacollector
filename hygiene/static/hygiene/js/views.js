/* global jQuery, Backbone, _, config */
(function ($, Backbone, _, config) {

    config.views = {};

    config.views.LoginView = Backbone.View.extend({
        el: '#login',
        events: {
            'submit': 'submit'
        },
        submit: function (e) {
            e.preventDefault();
            var data = {
                username: $(':input[name="username"]', this.$el).val(),
                password: $(':input[name="password"]', this.$el).val()
            };
            $('.error', this.$el).remove();
            $.post(this.$el.attr('action'), data)
                .done($.proxy(this.login, this))
                .fail($.proxy(this.fail, this));
        },
        login: function (result) {
            this.trigger('login', result.token);
            this.$el.hide();
        },
        fail: function () {
            this.$el.prepend('<p class="error">Invalid username/password</p>');
        }
    });

    config.views.QuestionFormView = Backbone.View.extend({
        el: '#collect',
        render: function () {
            this.$el.show();
        }
    });

    config.views.ResultsView = Backbone.View.extend({
        el: '#results',
        render: function () {
            this.$el.show();
        }
    });

})(jQuery, Backbone, _, config);
