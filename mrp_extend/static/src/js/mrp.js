odoo.define('mrp_extend.mrp_bom_report', function (require) {
    'use strict';

    var core = require('web.core');
    var stock_report_generic = require('mrp.mrp_bom_report');
    var framework = require('web.framework');
    // var stock_report_generic = require('stock.stock_report_generic');
    var QWeb = core.qweb;
    var aja = stock_report_generic.include({
        renderSearch: function () {
            this.$buttonPrint = $(QWeb.render('mrp.button'));
            this.$buttonPrint.find('.o_mrp_bom_print').on('click', this._onClickPrint.bind(this));
            this.$buttonPrint.find('.o_mrp_bom_print_unfolded').on('click', this._onClickPrint.bind(this));
            this.$buttonPrint.find('.o_mrp_bom_print_unfoldedddd').on('click', this._onClickPrinter.bind(this));
            this.$searchView = $(QWeb.render('mrp.report_bom_search', _.omit(this.data, 'lines')));
            this.$searchView.find('.o_mrp_bom_report_qty').on('change', this._onChangeQty.bind(this));
            this.$searchView.find('.o_mrp_bom_report_variants').on('change', this._onChangeVariants.bind(this));
            this.$searchView.find('.o_mrp_bom_report_type').on('change', this._onChangeType.bind(this));
        },



        _onClickPrinter: function (ev) {
            var childBomIDs = _.map(this.$el.find('.o_mrp_bom_foldable').closest('tr'), function (el) {
                return $(el).data('id');
            });

            var reportname = 'mrp.report_bom_structure?docids=' + this.given_context.active_id +
                '&report_type=' + this.given_context.report_type +
                '&quantity=' + (this.given_context.searchQty || 1);

            if (ev.currentTarget.className == 'btn btn-primary o_mrp_bom_print_unfoldedddd') {
                reportname += '&excel=' + 'excel';
                console.log("aaaa")
            }

            return this.do_action({
                type: 'ir.actions.act_window',
                name: 'Exportar Reporte',
                res_model: 'mrp.wizard.xls',
                view_mode: 'form',
                target: 'new',
                views: [[false, 'form']],
                context: {
                    'otro': 'reportname',
                    'id_active':this.given_context.active_id,
                    'ms': childBomIDs,
                    'json': JSON.stringify(childBomIDs),
                },

            })
            

        },

        // _onClickPrint: function (ev) {
        //     var childBomIDs = _.map(this.$el.find('.o_mrp_bom_foldable').closest('tr'), function (el) {
        //         return $(el).data('id');
        //     });
        //     framework.blockUI();
        //     var reportname = 'mrp.report_bom_structure?docids=' + this.given_context.active_id +
        //         '&report_type=' + this.given_context.report_type +
        //         '&quantity=' + (this.given_context.searchQty || 1);
        //     if (!$(ev.currentTarget).hasClass('o_mrp_bom_print_unfolded')) {
        //         reportname += '&childs=' + JSON.stringify(childBomIDs);
        //     }
        //     if (ev.currentTarget.className == 'btn btn-primary o_mrp_bom_print_unfoldedddd') {
        //         reportname += '&excel=' + 'excel';
        //         console.log("aaaa")
        //     }
        //     if (this.given_context.searchVariant) {
        //         reportname += '&variant=' + this.given_context.searchVariant;
        //     }
        //     console.log(this.given_contex)
        //     console.log(reportname)

        //     var action = {
        //         'type': 'ir.actions.report',
        //         'report_type': 'qweb-pdf',
        //         'report_name': reportname,
        //         'report_file': 'mrp.report_bom_structure',

        //     };
        //     return this.do_action(action).then(function () {
        //         framework.unblockUI();
        //     });
        // },

    });



    core.action_registry.add('mrp.mrp_bom_report', aja);
    return aja;




});