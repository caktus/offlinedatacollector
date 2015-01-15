/* global jQuery, Backbone, _ */
var config = (function ($, Backbone, _) {

    $(document).ready(function () {
        var loginView = new config.views.LoginView();

        loginView.on('login', function (token) {
            $.ajaxPrefilter(function (settings, options, xhr) {
                xhr.setRequestHeader('Authorization', 'Bearer ' + token);
            });
            // TODO: Render the question
        });
    });

    return JSON.parse($('#config').text());

})(jQuery, Backbone, _);
