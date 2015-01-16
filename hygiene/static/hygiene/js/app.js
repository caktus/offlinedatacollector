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
            // TODO: Determine if question or results should be shown
            formView.render();
        });
    });

    return JSON.parse($('#config').text());

})(jQuery, Backbone, _);
