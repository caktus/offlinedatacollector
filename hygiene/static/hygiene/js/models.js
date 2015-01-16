/* global jQuery, Backbone, _, config */
(function ($, Backbone, _, config) {

    function getTodayString() {
        var today = new Date();
        return today.toISOString().replace(/T.*/g, '');
    }

    var Cleaning = Backbone.Model.extend({
        defaults: function () {
            var today = new Date();
            return {
                date: getTodayString()
            };
        },
        url: function () {
            var links = this.get('links'),
                url = links && links.self;
            if (!url) {
                url = Backbone.Model.prototype.url.call(this);
            }
            return url;
        },
        date: function () {
            return new Date(this.get('date'));
        },
        isToday: function () {
            return this.get('date') === getTodayString();
        }
    });

    config.collections = {};
    config.collections.Cleanings = Backbone.Collection.extend({
        model: Cleaning,
        url: config.api,
        parse: function (response) {
            this._next = response.next;
            this._previous = response.previous;
            this._count = response.count;
            return response.results || [];
        }
    });

})(jQuery, Backbone, _, config);
