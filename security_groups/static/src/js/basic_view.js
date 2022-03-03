odoo.define('security_groups.BasicView', function (require) {
        "use strict";
        
        var session = require('web.session');
        var ListView = require('web.ListView');
        var FormView = require('web.FormView');
        var view_registry = require('web.view_registry');
    
        var CustomListView = ListView.extend({
            init: function(viewInfo, params) {
                this._super.apply(this, arguments);
                var self = this;
                session.user_has_group('security_groups.group_rol_1').then(function(has_group) {
                    if(has_group) {
                        self.controllerParams.archiveEnabled = false;
                    }
                });
            }   
        });
    
        var CustomFormView = FormView.extend({
            init: function(viewInfo, params) {
                this._super.apply(this, arguments);
                var self = this;
                session.user_has_group('security_groups.group_rol_1').then(function(has_group) {
                    if(has_group) {
                        self.controllerParams.archiveEnabled = false;
                    }
                });
            }   
        });
        view_registry.add('custom-form-view-stock', CustomFormView);
        view_registry.add('custom-list-view-stock', CustomListView);
    
        });