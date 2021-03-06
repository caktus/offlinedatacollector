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
        },
        render: function () {
            var token = localStorage.token;
            if (token) {
                this.login({token: token});
            } else {
                this.$el.fadeIn();
                this.listenToOnce(this, 'login', function (value) {
                    localStorage.token = value;
                });
            }
        }
    });

    config.views.QuestionFormView = Backbone.View.extend({
        el: '#collect',
        events: {
            'click button': 'submit'
        },
        submit: function (e) {
            e.preventDefault();
            var button = $(e.currentTarget),
                attributes = {
                    completed: button.attr('name') === 'yes'
                };
            this.collection.create(attributes, {
                success: $.proxy(this.success, this),
                error: $.proxy(this.failure, this)
            });
        },
        render: function () {
            this.$el.fadeIn();
        },
        success: function (model) {
            // TODO: Add messaging to the user
            this.$el.hide();
        },
        failure: function () {
            // TODO: Client messed up and is trying to create duplicate.
        }
    });

    config.views.ResultsView = Backbone.View.extend({
        el: '#results',
        template: _.template('<%- count %> day<% if (count !== 1) { %>s<% } %>'),
        initialize: function () {
            this.listenTo(this.collection, 'add', this.maybeRender);
        },
        maybeRender: function (model) {
            if (model.isToday()) {
                this.render();
            }
        },
        render: function () {
            var streak = this.collection.currentStreak(),
                html = this.template({count: streak}),
                msg = $('.count', this.$el);
            msg.html(html);
            if (streak === 0) {
                msg.addClass('empty');
            } else {
                 msg.removeClass('empty');
            }
            this.$el.fadeIn();
        }
    });

})(jQuery, Backbone, _, config);
