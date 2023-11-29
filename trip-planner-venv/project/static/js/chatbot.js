//@ts-nocheck
"use strict";
(function ($) {
    console.log('Loaded');
    var container;
    $.fn.chunkosChat = function (options) {
        // override options with user preferences
        var settings = $.extend({
            delay: 1500,
            autoStart: true,
            startMessageId: 1,
            dataJSON: null
        }, options);
        container = $(this);

        startChat(container, settings.dataJSON, settings.startMessageId, settings.delay)
    }

    function startChat(container, data, startId, delay) {
        container.html('<div class="chat-inner"></div>');
        var message = findMessageInJsonById(data, startId);
        generateMessageHTML(container, data, message, delay);
    }

    function findMessageInJsonById(data, id) {
        var messages = data;
        let msg = messages.filter((el) => {
            return el.id == id
        })[0]
        if (msg) {
            return msg;
        }
    }

    function toggleLoader(status, container) {
        if (status == "show") {
            container.children('.chat-inner').append(`<div class="message-wrapper typing"><div class="typing-indicator"><span></span><span></span><span></span></div></div>`);
        }
        else {
            container.find('.typing').remove();
        }
    }

    function generateMessageHTML(container, messages, m, delay) {
        var $template = $(`<div class="message-wrapper"><div class="chat-bubble left img"><img src="${m.imageUrl}" alt="" width="60" height="60" class="img-fluid"></div></div>`);
        m?.texts.forEach(el => {
            let $textElm = $(`<div class="chat-bubble left">${el?.text}</div>`);
            $template.append($textElm);
        })        
        toggleLoader("show", container);
        container.scrollTop(container.prop('scrollHeight'));
        setTimeout(function () {
            toggleLoader("hide", container);
            container.children('.chat-inner').append($template);
            container.scrollTop(container.prop('scrollHeight'));
            if (m.nextMessageId != "") {
                var nextMessage = findMessageInJsonById(messages, m.nextMessageId)
                generateMessageHTML(container, messages, nextMessage, delay)
            }
        }, delay);
        // end delay
    }

    function processUserMessage(userMessage) {

        $.get("questions.json", function(dataJSON) { 
            var preDefinedMessage = findMessageInJsonById(dataJSON, 3);
            if (preDefinedMessage) {
                generateMessageHTML(container, dataJSON, preDefinedMessage, 1500)
            }

            
        });
    }

    $(function () {
        $.get("questions.json", function (dataJSON) {
            $('#chat-app').chunkosChat({
                dataJSON: dataJSON,
            });

        });
    });

    $('#user-input-form').on('submit', function(e) {
        e.preventDefault(); // Prevents the default form submission action
        var userMessage = $('#user-message').val().trim();

        if (userMessage !== '') {
                // Append the message to the chat window or handle it as required
                var userMessageHTML = `<div class="message-wrapper"><div class="chat-bubble right">${userMessage}</div></div>`;
                $('.chat-app .chat-inner').append(userMessageHTML);
                processUserMessage(userMessage);
                $('#user-message').val(''); // Clear the input field after sending the message
        }
    });
}(jQuery));