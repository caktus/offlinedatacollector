/* global jQuery, Backbone, _, config */
(function ($, Backbone, _, config) {

    function getDatePart(date) {
        return date.toISOString().replace(/T.*/g, '');
    }

    function getTodayString() {
        var today = new Date();
        return getDatePart(today);
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
        comparator: 'date',
        parse: function (response) {
            this._next = response.next;
            this._previous = response.previous;
            this._count = response.count;
            return response.results || [];
        },
        currentStreak: function () {
            var streak = 0,
                found = true,
                current = new Date();
            while (found) {
                found = this.findWhere({date: getDatePart(current)});
                if (found) {
                    if (found.get('completed')) {
                        streak = streak + 1;
                    } else {
                        found = false;
                    }
                    current.setDate(current.getDate() - 1);
                }
            }
            return streak;
        }
    });

})(jQuery, Backbone, _, config);
