/* global jQuery, Backbone, _ */
var config = (function ($, Backbone, _) {

    $(document).ready(function () {
        var loginView = new config.views.LoginView();

        loginView.on('login', function (token) {
            var cleanings = new config.collections.Cleanings(),
                formView = new config.views.QuestionFormView({collection: cleanings}),
                resultsView = new config.views.ResultsView({collection: cleanings});
            $.ajaxPrefilter(function (settings, options, xhr) {
                xhr.setRequestHeader('Authorization', 'Token ' + token);
            });
            cleanings.fetch({success: function () {
                var today = new Date();
                if (!cleanings.getForDate(today)) {
                    formView.render();
                }
            }});
        });

        loginView.render();
    });

    return JSON.parse($('#config').text());

})(jQuery, Backbone, _);
