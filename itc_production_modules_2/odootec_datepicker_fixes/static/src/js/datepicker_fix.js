openerp.odootec_datepicker_fixes = function (instance, m) {
    var _t = instance.web._t,
        QWeb = instance.web.qweb;
    var normalize_format = function (format) {
        return Date.normalizeFormat(instance.web.strip_raw_chars(format));
    };
    instance.web.parse_value = function (value, descriptor, value_if_empty) {
        var date_pattern = normalize_format(_t.database.parameters.date_format),
            time_pattern = normalize_format(_t.database.parameters.time_format);
        switch (value) {
            case false:
            case "":
                return value_if_empty === undefined ? false : value_if_empty;
        }
        var tmp;
        switch (descriptor.widget || descriptor.type || (descriptor.field && descriptor.field.type)) {
            case 'integer':
                do {
                    tmp = value;
                    value = value.replace(instance.web._t.database.parameters.thousands_sep, "");
                } while (tmp !== value);
                tmp = Number(value);
                // do not accept not numbers or float values
                if (isNaN(tmp) || tmp % 1)
                    throw new Error(_.str.sprintf(_t("'%s' is not a correct integer"), value));
                return tmp;
            case 'float':
                var tmp2 = value;
                do {
                    tmp = tmp2;
                    tmp2 = tmp.replace(instance.web._t.database.parameters.thousands_sep, "");
                } while (tmp !== tmp2);
                var reformatted_value = tmp.replace(instance.web._t.database.parameters.decimal_point, ".");
                var parsed = Number(reformatted_value);
                if (isNaN(parsed))
                    throw new Error(_.str.sprintf(_t("'%s' is not a correct float"), value));
                return parsed;
            case 'float_time':
                var factor = 1;
                if (value[0] === '-') {
                    value = value.slice(1);
                    factor = -1;
                }
                var float_time_pair = value.split(":");
                if (float_time_pair.length != 2)
                    return factor * instance.web.parse_value(value, {type: "float"});
                var hours = instance.web.parse_value(float_time_pair[0], {type: "integer"});
                var minutes = instance.web.parse_value(float_time_pair[1], {type: "integer"});
                return factor * (hours + (minutes / 60));
            case 'progressbar':
                return instance.web.parse_value(value, {type: "float"});
            case 'datetime':
                var datetime = Date.parseExact(
                    value, (date_pattern + ' ' + time_pattern));
                if (datetime !== null)
                    return instance.web.datetime_to_str(datetime);
                datetime = Date.parseExact(value, (date_pattern));
                if (datetime !== null)
                    return instance.web.datetime_to_str(datetime);
                var leading_zero_value = value.toString().replace(/\d+/g, function (m) {
                    return m.length === 1 ? "0" + m : m;
                });
                datetime = Date.parseExact(leading_zero_value, (date_pattern + ' ' + time_pattern));
                if (datetime !== null)
                    return instance.web.datetime_to_str(datetime);
                datetime = Date.parseExact(leading_zero_value, (date_pattern));
                if (datetime !== null)
                    return instance.web.datetime_to_str(datetime);
                datetime = Date.parse(value);
                if (datetime !== null)
                    return instance.web.datetime_to_str(datetime);
                return instance.web.datetime_to_str(datetime);
            case 'date':
                var date = Date.parseExact(value, date_pattern);
                if (date !== null)
                    return instance.web.date_to_str(date);
                date = Date.parseExact(value.toString().replace(/\d+/g, function (m) {
                    return m.length === 1 ? "0" + m : m;
                }), date_pattern);
                if (date !== null)
                    return instance.web.date_to_str(date);
                date = Date.parse(value);
                if (date !== null)
                    return instance.web.date_to_str(date);
                return instance.web.date_to_str(date);
            case 'time':
                var time = Date.parseExact(value, time_pattern);
                if (time !== null)
                    return instance.web.time_to_str(time);
                time = Date.parse(value);
                if (time !== null)
                    return instance.web.time_to_str(time);
                return instance.web.time_to_str(time);
        }
        return value;
    };
    instance.web.ListView.List.include({
        convert_gregorian_hijri: function (text) {

            if (text) {
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
            if (column.type === 'date') {
                return column.format(record.toForm().data, {
                        model: this.dataset.model,
                        id: record.get('id')
                    }) + "&nbsp; &nbsp; &nbsp;" + this.convert_gregorian_hijri(column.format(record.toForm().data, {
                        model: this.dataset.model,
                        id: record.get('id')
                    }));
            }
            if (column.type === 'reference') {
                value = record.get(column.id);
                var ref_match;
                if (value && (ref_match = /^([\w\.]+),(\d+)$/.exec(value))) {
                    var model = ref_match[1],
                        id = parseInt(ref_match[2], 10);
                    new instance.web.DataSet(this.view, model).name_get([id]).done(function (names) {
                        if (!names.length) {
                            return;
                        }
                        record.set(column.id + '__display', names[0][1]);
                    });
                }
            } else if (column.type === 'many2one') {
                value = record.get(column.id);
                if (typeof value === 'number' || value instanceof Number) {
                    new instance.web.DataSet(this.view, column.relation)
                        .name_get([value]).done(function (names) {
                        if (!names.length) {
                            return;
                        }
                        record.set(column.id, names[0]);
                    });
                }
            } else if (column.type === 'many2many' || column.type === 'one2many') {
                value = record.get(column.id);
                if (value instanceof Array && !_.isEmpty(value)
                    && !record.get(column.id + '__display')) {
                    var ids;
                    if (value[0] instanceof Array) {
                        var command = value[0];
                        if (command[0] !== 6) {
                            throw new Error(_.str.sprintf(_t("Unknown m2m command %s"), command[0]));
                        }
                        ids = command[2];
                    } else {
                        ids = value;
                    }
                    new instance.web.Model(column.relation)
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
}