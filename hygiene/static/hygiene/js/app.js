/* global jQuery, Backbone, _ */
var config = (function ($, Backbone, _) {

    $(document).ready(function () {
        var loginView = new config.views.LoginView(),
            formView = new config.views.QuestionFormView(),
            resultsView = new config.views.ResultsView();

        loginView.on('login', function (token) {
            $.ajaxPrefilter(function (settings, options, xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer ' + token);
            });
            // TODO: Determine if question or results should be shown
            formView.render();
        });
    });

    return JSON.parse($('#config').text());

})(jQuery, Backbone, _);
