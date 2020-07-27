odoo.define('khmerrealty.website_effect', function (require) {
'use strict';
    var core = require('web.core');
    var wUtils = require('website.utils');
    var publicWidget = require('web.public.widget');
    var _t = core._t;
    publicWidget.registry.websiteRealtyHome = publicWidget.Widget.extend({
        selector: '.o_wrealty',
        events: {
            'click ul.form_search_label li': '_onClickSearchLabel',
            'click #o_website_realtysearch ul.search_label li': '_onClickSearchLabelPropertyListing',
            'click ul.news_events_tap_title li': '_onClickNewsEventLabel',
            'click ul.property_tab_label li': '_onClickNewsEventLabel'
        },

        /**
         * @override
         */
        start: function () {
            $('.property_rent_content').hide();
            return this._super.apply(this, arguments);
        },

        _onClickSearchLabel: function(evt){
            evt.preventDefault();
            $(evt.currentTarget).addClass('active').siblings().removeClass('active');
            $('#search_property_type').val(evt.currentTarget.dataset.type);
            $('#search_text').attr("placeholder",evt.currentTarget.dataset.holder);
        },

        _onClickNewsEventLabel: function(evt){
            evt.preventDefault();
            $(evt.currentTarget).addClass('btn btn-primary').siblings().removeClass('btn btn-primary');
            $('.'+evt.currentTarget.dataset.target).show('fast','swing').siblings().hide();
        },

        _onClickSearchLabelPropertyListing: function(evt){
            evt.preventDefault();
            $(evt.currentTarget).addClass('active').siblings().removeClass('active');
            $('#search_property_type').val(evt.currentTarget.dataset.type);
            $('#search_text').attr("placeholder",evt.currentTarget.dataset.holder);
        },

    });
    publicWidget.registry.websiteRealtySearchForm = publicWidget.Widget.extend({
        selector: '#slide #search_form',
        events: {
            'click ul.form_search_label li': '_showSearchForm',
        },
        start: function(){
            return this._super.apply(this, arguments);
        },

        _showSearchForm: function(evt){
            evt.preventDefault();
            $(evt.currentTarget).addClass('active').siblings().removeClass('active');
            $('#search_property_type').val(evt.currentTarget.dataset.type);
            $('#search_text').attr("placeholder",evt.currentTarget.dataset.holder);
        }
    });
    publicWidget.registry.khmerrealty_js = publicWidget.Widget.extend({
        selector: '#o_guides_and_news_block',
        events: {
            'click li.guides': '_showGuides',
            'click li.news': '_showNews',
            'click #tab_buy_property': '_showBuyProperty',
            'click #tab_rent_property': '_showRentProperty',
        },

        start: function () {
            $('.guides_content').hide();
            $('li.news').addClass('active');
            $('.o_header_affix #slide').empty();
            $('[data-fancybox="preview"]').fancybox({
              thumbs : {
                autoStart : true
              }
            });

            return this._super.apply(this, arguments);
        },
        _showGuides: function(evt){
            var self = this;
            evt.preventDefault();
            $(evt.currentTarget).addClass('active').siblings().removeClass('active');
            $('.'+evt.currentTarget.dataset.target).show().siblings().hide();
        },
        _showNews: function(evt){
            var self= this;
            evt.preventDefault();
            $(evt.currentTarget).addClass('active').siblings().removeClass('active');
            $('.'+evt.currentTarget.dataset.target).show().siblings().hide();
        },
        _removeActiveClass: function(options){
            _.each(options, function(option){
                console.log($(option));
            });
        },
    });

    publicWidget.registry.khmerrealty_buyorrent_tab = publicWidget.Widget.extend({
        selector: '#feature_property_home_page',
        events: {
            'click #tab_buy_property': '_showBuyProperty',
            'click #tab_rent_property': '_showRentProperty',
        },
        start: function(){
            $('ul.popular_property_tab li:first-child').addClass('active');
            $('#popular_property_content_rent').hide();
            return this._super.apply(this, arguments);
        },
        _showBuyProperty: function(evt){
            var self= this;
            $(evt.currentTarget).addClass('active').siblings().removeClass('active');
            $('#'+evt.currentTarget.dataset.target).show().siblings().hide();
        },

        _showRentProperty: function(evt){
            var self= this;
            $(evt.currentTarget).addClass('active').siblings().removeClass('active');
            $('#'+evt.currentTarget.dataset.target).show().siblings().hide();
        },

    });

    publicWidget.registry.khmerrealty_search_tab = publicWidget.Widget.extend({
        selector: '#search_top',
        events: {
            'click #buy_tab': '_showBuyContent',
            'click #rent_tab': '_showRentContent',
            'click #apartment_tab': '_showApartmentContent',
            'click #development_tab': '_showDevelopmentContent',
            'click #land_tab': '_showLandContent',
        },

        start: function(){
            $('li.buy').addClass('active');
            $('li#rent_content').hide();
            $('li#apartment_content').hide();
            $('li#development_content').hide();
            $('li#land_content').hide();
            return this._super.apply(this, arguments);
        },

        _showRentContent: function(evt){
            evt.preventDefault();
            $(evt.currentTarget.parentElement).addClass('active').siblings().removeClass('active');
            $(evt.currentTarget.hash).show().siblings().hide();
        },

        _showBuyContent: function(evt){
            evt.preventDefault();
            $(evt.currentTarget.parentElement).addClass('active').siblings().removeClass('active');
            $(evt.currentTarget.hash).show().siblings().hide();
        },
        _showApartmentContent: function(evt){
            evt.preventDefault();
            $(evt.currentTarget.parentElement).addClass('active').siblings().removeClass('active');
            $(evt.currentTarget.hash).show().siblings().hide();
        },
        _showDevelopmentContent: function(evt){
            evt.preventDefault();
            $(evt.currentTarget.parentElement).addClass('active').siblings().removeClass('active');
            $(evt.currentTarget.hash).show().siblings().hide();
        },
        _showLandContent: function(evt){
            evt.preventDefault();
            $(evt.currentTarget.parentElement).addClass('active').siblings().removeClass('active');
            $(evt.currentTarget.hash).show().siblings().hide();
        },
    });

    publicWidget.registry.khmerrealty_go_to_top = publicWidget.Widget.extend({
        selector: '#right_dock',
        events: {
            'click p#goto_top_click': '_gotoTop',
            'click li.go_to_top': '_gotoTop',
        },
        start: function () {
            var gototop = $('li.go_to_top');
            $(window).scroll(function() {
              if ($(window).scrollTop() > 300) {
                gototop.css('display', 'block');
              } else {
                gototop.css('display', 'none');
              }
            });
            return this._super.apply(this, arguments);
        },
        _gotoTop: function(evt){
            var self = this;
            evt.preventDefault();
            $('html, body').animate({scrollTop:0}, '300');
        }
    });

    publicWidget.registry.khmerrealty_share = publicWidget.Widget.extend({
        selector: '#single_property',
        events: {
            'click .o_facebook': '_showShare',
        },

        start: function () {
            return this._super.apply(this, arguments);
        },
        _showShare: function(evt){
            evt.preventDefault();
            var url = '';
            var $element = $(evt.currentTarget);
            var blogPostTitle = encodeURIComponent($('#property_name span.name').html() || '');
            var articleURL = encodeURIComponent(window.location.href);
            if ($element.hasClass('o_facebook')) {
                url = 'https://www.facebook.com/sharer/sharer.php?u=' + articleURL;
            }
            window.open(url, '', 'menubar=no, width=500, height=400');
        },
    });

    publicWidget.registry.khmerrealty_change_location = publicWidget.Widget.extend({
        selector: 'form#property_by_location_form',
        events: {
            'change #property_by_location_js': '_showPropertyByLocation',
        },

        start: function () {
            return this._super.apply(this, arguments);
        },
        _showPropertyByLocation: function(evt){
            $('#search_location_js_submit_button').click();
        },
    });
});