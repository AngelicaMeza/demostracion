odoo.define('monetary_conversion_fix.FormatMonetary', require => {
    'use strict';

    const field_utils = require('web.field_utils');
    const core = require('web.core');
    const dom = require('web.dom');
    const session = require('web.session');
    const time = require('web.time');
    const utils = require('web.utils');
    
    function formatFloat(value, field, options) {
        options = options || {};
        if (value === false) {
            return "";
        }
        if (options.humanReadable && options.humanReadable(value)) {
            return utils.human_number(value, options.decimals, options.minDigits, options.formatterCallback);
        }
        var l10n = core._t.database.parameters;
        var precision;
        if (options.digits) {
            precision = options.digits[1];
        } else if (field && field.digits) {
            precision = field.digits[1];
        } else {
            precision = 2;
        }
        var formatted = _.str.sprintf('%.' + precision + 'f', value || 0).split('.');
        formatted[0] = utils.insert_thousand_seps(formatted[0]);
        return formatted.join(l10n.decimal_point);
    }
    


    function formatMonetaryFix(value, field, options) {
        if (value === false) {
            return "";
        }
        options = options || {};
    
        var currency = options.currency;
        if (!currency) {
            var currency_id = options.currency_id;
            if (!currency_id && options.data) {
                var currency_field = options.currency_field || field.currency_field || 'currency_id';
                currency_id = options.data[currency_field] && options.data[currency_field].res_id;
            }
            currency = session.get_currency(currency_id);
        }
    
        var digits = (currency && currency.digits) || options.digits;
        if (options.field_digits === true) {
            digits = field.digits || digits;
        }
        var formatted_value = formatFloat(value, field,
            _.extend({}, options , {digits: [69,2]})
        );
    
        if (!currency || options.noSymbol) {
            return formatted_value;
        }
        if (currency.position === "after") {
            return formatted_value += '&nbsp;' + currency.symbol;
        } else {
            return currency.symbol + '&nbsp;' + formatted_value;
        }
    }

    field_utils.format.monetary = formatMonetaryFix;
});