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
                wait: true,
                success: $.proxy(this.success, this),
                error: $.proxy(this.failure, this)
            });
        },
        render: function () {
            this.$el.show();
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
            var context = {count: this.collection.currentStreak()},
                html = this.template(context);
            $('.streak', this.$el).html(html);
            this.$el.show();
        }
    });

})(jQuery, Backbone, _, config);
