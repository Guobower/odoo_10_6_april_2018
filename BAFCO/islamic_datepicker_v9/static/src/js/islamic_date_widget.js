odoo.define('islamic_datepicker_v9.islamic_date_widget', function (require) {
    var Model = require('web.Model');
    var core = require('web.core');
    var ListView = core.view_registry.get('list')
    var FieldDateTime = core.form_widget_registry.get('datetime');
    var datepicker = require('web.datepicker');
    var formats = require('web.formats');
    var data = require('web.data');
    var res_users = new Model("res.users");
    var lang = '';
    var date_format = '';
    res_users.call("datepicker_localization", []).then(function (result) {
        lang = result['lang'];
        date_format = result['date_format'];
        date_format = date_format.replace(/%(.)/g, "$1$1").toLowerCase();
        ;
    });
    ListView.List.include({
        convert_gregorian_hijri: function (text) {
            if (text) {
                text = moment(text, date_format)._i;
                if (text.indexOf('-') != -1) {
                    text_split = text.split('-');
                    year = parseInt(text_split[0]);
                    month = parseInt(text_split[1]);
                    day = parseInt(text_split[2]);
                    calendar = $.calendars.instance('gregorian');
                    calendar1 = $.calendars.instance('islamic');
                    var jd = $.calendars.instance('gregorian').toJD(year, month, day);
                    var date = $.calendars.instance('islamic').fromJD(jd);
                }
                if (text.indexOf('/') != -1) {
                    text_split = text.split('/');
                    year = parseInt(text_split[2]);
                    month = parseInt(text_split[0]);
                    day = parseInt(text_split[1]);
                    calendar = $.calendars.instance('gregorian');
                    calendar1 = $.calendars.instance('islamic');
                    var jd = calendar.toJD(year, month, day);
                    var date = calendar1.fromJD(jd);
                }
                return (calendar1.formatDate('M d, yyyy', date));
            }
            return '';
        },
        render_cell: function (record, column) {
            var value;
            if (column.type === 'date' || column.type === 'datetime') {
                return column.format(record.toForm().data, {
                        model: this.dataset.model,
                        id: record.get('id')
                    }) + "&nbsp; &nbsp; &nbsp;" + this.convert_gregorian_hijri(column.format(record.toForm().data, {
                        model: this.dataset.model,
                        id: record.get('id')
                    }));
            }
            else if (column.type === 'reference') {
                value = record.get(column.id);
                var ref_match;
                if (value && (ref_match = /^([\w\.]+),(\d+)$/.exec(value))) {
                    var model = ref_match[1],
                        id = parseInt(ref_match[2], 10);
                    new data.DataSet(this.view, model).name_get([id]).done(function (names) {
                        if (!names.length) {
                            return;
                        }
                        record.set(column.id + '__display', names[0][1]);
                    });
                }
            } else if (column.type === 'many2one') {
                value = record.get(column.id);

                if (typeof value === 'number' || value instanceof Number) {

                    new data.DataSet(this.view, column.relation)
                        .name_get([value]).done(function (names) {
                        if (!names.length) {
                            return;
                        }
                        record.set(column.id, names[0]);
                    });
                }
            } else if (column.type === 'many2many') {
                value = record.get(column.id);
                if (value instanceof Array && !_.isEmpty(value)
                    && !record.get(column.id + '__display')) {
                    var ids;
                    if (value[0] instanceof Array) {
                        _.each(value, function (command) {
                            switch (command[0]) {
                                case 4:
                                    ids.push(command[1]);
                                    break;
                                case 5:
                                    ids = [];
                                    break;
                                case 6:
                                    ids = command[2];
                                    break;
                                default:
                                    throw new Error(_.str.sprintf(_t("Unknown m2m command %s"), command[0]));
                            }
                        });
                    } else {
                        ids = value;
                    }
                    new Model(column.relation)
                        .call('name_get', [ids, this.dataset.get_context()]).done(function (names) {

                        record.set(column.id + '__display',
                            _(names).pluck(1).join(', '));
                        record.set(column.id, ids);
                    });
                    record.set(column.id, false);
                }
            }
            return column.format(record.toForm().data, {
                model: this.dataset.model,
                id: record.get('id')
            });
        },
    });
    datepicker.DateWidget.include({
        start: function () {
            this.$input = this.$el.find('input.oe_simple_date');
            this.$input_picker = this.$el.find('input.oe_datepicker_container');
            this.$input_hijri = this.$el.find('input.oe_hijri');
            $(this.$input_hijri).val('')
            this._super();
            this.$input = this.$el.find('input.oe_simple_date');
        },
        convert_gregorian_hijri: function (text) {
            if (text) {
                text = moment(text, date_format)._i;
                if (text.indexOf('-') != -1) {
                    text_split = text.split('-');
                    year = parseInt(text_split[0]);
                    month = parseInt(text_split[1]);
                    day = parseInt(text_split[2]);
                    calendar = $.calendars.instance('gregorian');
                    calendar1 = $.calendars.instance('islamic');
                    var jd = calendar.toJD(year, month, day);
                    var date = calendar1.fromJD(jd);
                }
                if (text.indexOf('/') != -1) {
                    text_split = text.split('/');
                    year = parseInt(text_split[2]);
                    month = parseInt(text_split[0]);
                    day = parseInt(text_split[1]);
                    calendar = $.calendars.instance('gregorian');
                    calendar1 = $.calendars.instance('islamic');
                    var jd = calendar.toJD(year, month, day);
                    var date = calendar1.fromJD(jd);
                }
                m = (date.month() >= 10 ? date.month() : "0" + date.month());
                d = (date.day() >= 10 ? date.day() : "0" + date.day());

                $(this.$input_hijri).val(calendar1.formatDate('M d, yyyy', date));

                $(".o_datepicker input:last").click(function (event) {
                    event.stopPropagation();
                    $('.oe_hijri').calendarsPicker({
                        calendar: $.calendars.instance('islamic', lang),
                        dateFormat: 'M d, yyyy',
                        onSelect: true,
                    });
                });
                $(this.$input_hijri).calendarsPicker({
                    calendar: $.calendars.instance('islamic', lang),
                    dateFormat: 'M d, yyyy',
                    onSelect: true,
                });
            }
        },

        set_value: function (value) {
            this._super(value);
            $(this.$input_hijri).val('')
            this.convert_gregorian_hijri(value);
            this.$input.val(value ? this.format_client(value) : '');
        },
        set_value_from_ui: function () {
            this._super();
            var value = this.$input.val() || false;
            this.value = this.parse_client(value);
            this.convert_gregorian_hijri(this.value);
        },
        set_readonly: function (readonly) {
            this._super(readonly);
            this.$input_hijri.prop('readonly', this.readonly);
        },
        change_datetime: function (e) {
            this.set_value_from_ui();
            this.trigger("datetime_changed");
        }

    });
    FieldDateTime.include({

        initialize_content: function () {

            if (!this.get("effective_readonly")) {
                this.datewidget = this.build_widget();
                this.datewidget.on('datetime_changed', this, _.bind(function () {
                    this.internal_set_value(this.datewidget.get_value());
                }, this));
                this.datewidget.appendTo(this.$el.find(".oe_simple_date")[0]);
                this.setupFocus(this.datewidget.$input);
                this.format = "%m/%d/%Y";
                showtime = false;
                this.calendar_format = this.field.type;

                this.datewidget.calendar_format = this.field.type;
                if (this.field.type == 'datetime') {
                    this.format = "%m/%d/%Y %H:%M:%S";
                    showtime = true
                }
                var self = this;

                function convert_date_hijri(date) {
                    console.log("date-----click here---------", parseInt(date[0].year()), parseInt(date[0].month()), parseInt(date[0].day()));
                    if (!date) {
                        return false
                    }
                    if (self.field.type == 'datetime') {
                        var jd = $.calendars.instance('islamic').toJD(parseInt(date[0].year()), parseInt(date[0].month()), parseInt(date[0].day()) + 1);
                        var date = $.calendars.instance('gregorian').fromJD(jd);
                        var date_value = new Date(parseInt(date.year()), parseInt(date.month()) - 1, parseInt(date.day()));
                        self.datewidget.$input.val($.datepicker.formatDate(date_format + ' 00:00:00', date_value));
                    }
                    else {
                        var jd = $.calendars.instance('islamic').toJD(parseInt(date[0].year()), parseInt(date[0].month()), parseInt(date[0].day()));
                        var date = $.calendars.instance('gregorian').fromJD(jd);
                        var date_value = new Date(parseInt(date.year()), parseInt(date.month()) - 1, parseInt(date.day()));
                        self.datewidget.$input.val($.datepicker.formatDate(date_format, date_value));

                    }
                    self.datewidget.change_datetime();
                }

                $(".o_datepicker input:last").click(function (event) {
                    event.stopPropagation();
                    $('.oe_hijri').calendarsPicker({
                        calendar: $.calendars.instance('islamic', lang),
                        dateFormat: 'M d, yyyy',
                        onSelect: convert_date_hijri,
                    });
                });
                $('.oe_hijri').calendarsPicker({
                    calendar: $.calendars.instance('islamic', lang),
                    dateFormat: 'M d, yyyy',
                    onSelect: convert_date_hijri,
                });
            }
            this.calendar_format = this.field.type;
        },
        convert_gregorian_hijri: function (text) {
            if (text) {
                text = moment(text, date_format)._i;
                if (text.indexOf('-') != -1) {
                    text_split = text.split('-');
                    year = parseInt(text_split[0]);
                    month = parseInt(text_split[1]);
                    day = parseInt(text_split[2]);
                    calendar = $.calendars.instance('gregorian');
                    calendar1 = $.calendars.instance('islamic');
                    var jd = $.calendars.instance('gregorian').toJD(year, month, day);
                    var date = $.calendars.instance('islamic').fromJD(jd);
                }
                if (text.indexOf('/') != -1) {
                    text_split = text.split('/');
                    year = parseInt(text_split[2]);
                    month = parseInt(text_split[0]);
                    day = parseInt(text_split[1]);
                    calendar = $.calendars.instance('gregorian');
                    calendar1 = $.calendars.instance('islamic');
                    var jd = calendar.toJD(year, month, day);
                    var date = calendar1.fromJD(jd);
                }
                return (calendar1.formatDate('M d, yyyy', date));
            }
            return '';
        },

        render_value: function () {
            if (!this.get("effective_readonly")) {
                this.datewidget.set_value(this.get('value'));
            }
            else {
                var date_value = openerp.web.format_value(this.get('value'), this, '');
                this.$el.find(".oe_simple_date").text(date_value);
                this.$el.find(".oe_hijri_date").text(this.convert_gregorian_hijri(this.get('value')));
            }
        }
    });

});