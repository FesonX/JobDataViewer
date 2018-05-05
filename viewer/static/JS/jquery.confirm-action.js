/*!
 * jQuery Confirm Action
 * https://github.com/sdelements/jquery-confirm-action
 *
 * Copyright 2015, Houssam Haidar
 * Released under the MIT license
 */

'use strict';

(function($) {

    //
    // Helpers
    //

    var each = function(iterable, callback, context) {
        $.each(iterable, context ? $.proxy(callback, context) : callback);
    };

    var map = function(iterable, callback, context) {
        return $.map(iterable, context ? $.proxy(callback, context) : callback);
    };

    //
    // Modal
    //

    var ConfirmActionModal = function(options) {

        this.options = options;

        this.init();

    };

    ConfirmActionModal.prototype = {

        constructor: ConfirmActionModal,

        styles: {
            overlay: {
                position: 'fixed',
                top: 0,
                right: 0,
                bottom: 0,
                left: 0,
                zIndex: 1000,
                backgroundColor: '#000000'
            },
            base: {
                width: '100%',
                height: '100%',
                position: 'fixed',
                top: 0,
                left: 0,
                bottom: 0,
                right: 0,
                zIndex: 1001,
                overflow: 'auto'
            },
            dialog: {
                backgroundColor: '#ffffff',
                width: '100%',
                maxWidth: '600px',
                margin: '40px auto',
                textAlign: 'center',
                fontSize: '14px',
                borderRadius: '3px',
                position: 'relative',
                zIndex: 1001
            },
            header: {
                padding: '30px'
            },
            title: {
                fontWeight: '300',
                fontSize: '20px',
                color: '#555555',
                lineHeight: '40px',
                marginBottom: '0'
            },
            close: {
                position: 'absolute',
                top: '-25px',
                right: '-25px',
                fontSize: '30px',
                color: '#f2f2f2',
                cursor: 'pointer'
            },
            content: {
                padding: '10px 40px 60px 40px',
                color: '#888888',
                fontSize: '16px',
                fontWeight: '300',
                lineHeight: '20px'
            },
            actions: {
                backgroundColor: '#f5f5f5',
                padding: '30px',
                borderRadius: '0 0 3px 3px'
            },
            button: {
                background: 'none',
                fontSize: '14px',
                color: '#aaaaaa',
                padding: '10px 40px',
                margin: '3px 6px',
                border: '1px #cccccc solid',
                borderRadius: '4px'
            },
            titles: {
                danger: {
                    color: '#e56657'
                },
                warning: {
                    color: '#ffb347'
                },
                success: {
                    color: '#77dd77'
                }
            },
            buttons: {
                danger: {
                    backgroundColor: '#e56657',
                    borderColor: '#e56657',
                    color: '#ffffff'
                },
                warning: {
                    backgroundColor: '#ffb347',
                    borderColor: '#ffb347',
                    color: '#ffffff'
                },
                success: {
                    backgroundColor: '#77dd77',
                    borderColor: '#77dd77',
                    color: '#ffffff'
                }
            },
            conditions: {
                width: '60%',
                textAlign: 'left',
                margin: '0 auto',
                marginTop: '20px'
            },
            label: {
                fontSize: '14px',
                color: '#aaaaaa',
                marginTop: '10px',
                display: 'block'
            },
            checkbox: {
                margin: '0 5px 0 0',
                verticalAlign: 'baseline'
            }
        },

        html: {
            overlay: '<div class="confirm-action-overlay" />',
            base: '<div class="confirm-action-modal" />',
            dialog: '<div class="confirm-action-modal-dialog" />',
            header: '<div class="confirm-action-modal-header" />',
            title: '<h2 class="confirm-action-modal-title">Confirm</h2>',
            close: '<span class="confirm-action-modal-close" data-confirm-action-close>&times;</span>',
            content: '<div class="confirm-action-modal-content" />',
            conditions: '<div class="confirm-action-modal-conditions" />',
            actions: '<div class="confirm-action-modal-actions" />',
            button: '<button class="confirm-action-modal-button">Confirm</button>',
            label: '<label class="confirm-action-label" />',
            checkbox: '<input type="checkbox" />',
            conditionText: '<span class="confirm-action-condition-text" />'
        },

        init: function() {

            this.components = {};

            each(this.html, function(key, html) {

                this.components['$' + key] = $(html).css(this.styles[key] || {});

            }, this);

            this.$overlay = this.components.$overlay.fadeTo(0, 0.5);

            this.components.$title
                .css(this.styles.titles[this.options.title.style || 'danger']);

            var $conditions = map(this.options.conditions, function(condition, key) {

                if (condition.type === 'checkbox') {
                    return this.components.$label.clone()
                        .append([
                            this.components.$checkbox.clone().attr('data-confirm-condition-id', key),
                            this.components.$conditionText.clone().text(condition.text || 'Are you sure?')
                        ]);
                }

            }, this);

            var $buttons = [
                this.components.$button.clone()
                    .text('取消')
                    .attr('data-confirm-action-close', true)
            ];

            each(this.options.actions, function(key, action) {

                $buttons.push(
                    this.components.$button.clone()
                        .attr('data-confirm-action-id', key)
                        .text(action.text)
                        .css(this.styles.buttons[action.style || 'danger'])
                );

            }, this);

            this.$element = this.components.$base.append([
                this.$overlay,
                this.components.$dialog.append([
                    this.components.$header.append([
                        this.components.$title,
                        this.components.$close
                    ]),
                    this.components.$content.append(
                        this.components.$conditions.append($conditions)
                    ),
                    this.components.$actions.append($buttons)
                ])
            ]);

            this.update();

        },

        setTitleAndMessage: function() {
            this.setContent(this.options.title, this.components.$title);
            this.setContent(this.options.message, this.components.$content);
        },

        setContent: function(options, container) {
            if (options.html) {
                var html = typeof options.html === 'function' ? options.html() : options.html;
                if ($.isArray(html)) {
                    html = html.join('\n');
                }
                container.html(html);
            }

            if (options.text) {
                var text = typeof options.text === 'function' ? options.text() : options.text;
                container.text(text);
            }
        },

        listen: function(sourceEvent) {

            var that = this;

            this.$element.delegate('[data-confirm-action-close]', 'click', $.proxy(this.close, this));

            this.$overlay.on('click', $.proxy(this.close, this));

            var confirm = function() {

                $(sourceEvent.target).trigger('click', true);

                that.close();

            };

            this.$element.find('[data-confirm-condition-id]').each(function() {

                $(this).on('change.confirm.condition', function() {

                    that.update();

                });

            });

            this.$element.find('[data-confirm-action-id]').each(function() {

                $(this).on('click.confirm.action', function(e) {

                    e.preventDefault();

                    var callback = that.options.actions[$(this).data('confirm-action-id')].callback;

                    if (typeof callback !== 'function') {

                        callback = $.fn.confirmAction.defaults.actions.confirm.callback;

                    }

                    callback(confirm, $.proxy(that.close, that));

                });

            });

        },

        update: function() {

            var that = this;

            each(this.options.actions, function(actionKey, action) {

                var disabled = false;

                each(action.conditions || [], function(key, condition) {

                    if (disabled) {

                        return;

                    }

                    if (!that.options.conditions[condition]) {

                        disabled = true;
                    }

                    if (that.options.conditions[condition].type === 'checkbox') {

                        if (!that.$element.find('[data-confirm-condition-id=' + condition + ']').is(':checked')) {

                            disabled = true;

                        }

                    }

                });

                that.$element.find('[data-confirm-action-id=' + actionKey + ']')
                    .prop('disabled', disabled)
                    .css('cursor', disabled ? 'not-allowed' : 'pointer')
                    .fadeTo(50, disabled ? .5 : 1);

            });

        },

        show: function(sourceEvent) {

            this.setTitleAndMessage();

            this.$element.appendTo('body');

            this.listen(sourceEvent || $.Event('click'));

        },

        close: function() {

            this.resetConditions();
            this.$element.remove();

        },

        resetConditions: function() {
            this.components.$conditions.find('input[type=checkbox]').prop('checked', false);
        }

    };

    //
    // Core
    //

    var ConfirmAction = function(element, options) {

        this.init(element, options);

    };

    ConfirmAction.prototype = {

        constructor: ConfirmAction,

        init: function(element, options) {

            this.options = options;

            this.$element = $(element);

            this.$element.on('click.confirm', $.proxy(this.intercept, this));

            this.modal = new ConfirmActionModal(this.options);

        },

        intercept: function(e, confirmed) {

            var that = this;

            var execute = function(run) {

                if (!run) {
                    return;
                }

                that.modal.show(e);

                if (confirmed !== true) {

                    e.preventDefault();
                    e.stopImmediatePropagation();

                }

            };

            if (typeof this.options.conditional === 'function') {

                this.options.conditional(execute);

                return;

            }

            execute(true);

        }

    };

    //
    // jQuery Plugin
    //
    $.fn.confirmAction = function(options) {

        return this.each(function() {
            var title;
            var message;

            if (typeof options.title === 'string' || typeof options.message === 'function') {
                title = options.title;
                delete options.title;
            }

            if (typeof options === 'string') {
                message = options;
            }

            if (typeof options.message === 'string' || typeof options.message === 'function') {
                message = options.message;
                delete options.message;
            }

            options = $.extend({}, $.fn.confirmAction.defaults, typeof options === 'object' && options);

            if (title) {
                options.title.text = message;
            }

            if (message) {
                options.message.text = message;
            }

            new ConfirmAction(this, options);
        });

    };

    $.fn.confirmAction.defaults = {
        title: {
            text: 'Warning',
            style: 'danger'
        },
        message: {
            text: 'Are you sure?'
        },
        actions: {
            confirm: {
                text: 'Confirm',
                style: 'danger',
                callback: function(confirm) {
                    confirm();
                }
            }
        },
        conditions: {}
    };

})(jQuery);
