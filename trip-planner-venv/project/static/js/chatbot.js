
"use strict";
(function ($) {
    var container;

    function fetchJsonData(callback) {
        $.get("/static/js/questions.json", function(dataJSON) {
            callback(dataJSON);
        });
    }

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
        var planner_imageUrl = "/static/images/planner_avatar.gif"
        var $template = $(`<div class="message-wrapper"><div class="chat-bubble left img"><img src="${planner_imageUrl}" alt="" width="60" height="60" class="img-fluid"></div></div>`);
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

        fetchJsonData(function(dataJSON) {
            var preDefinedMessage = findMessageInJsonById(dataJSON, 3);
            if (preDefinedMessage) {
                generateMessageHTML(container, dataJSON, preDefinedMessage, 1500)
            }       
        });
    }

    $(function () {
        fetchJsonData(function(dataJSON) {
            $('#chat-app').chunkosChat({
                dataJSON: dataJSON,
            });
        });
    });

    $('#user-input-form').on('submit', function(e) {
        e.preventDefault(); // Prevents the default form submission action
        var userMessage = $('#user-message').val().trim();
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        if (userMessage !== '') {
                // Append the message to the chat window or handle it as required
                validateUserInput(csrfToken, "Location", userMessage) 

                var user_imageUrl = "/static/images/user_avatar.png"
                var $msgTemplate = $(`<div class="message-wrapper"><div class="chat-bubble right img"><img src="${user_imageUrl}" alt="" width="60" height="60" class="img-fluid"></div></div>`);
                var userMessageHTML = `<div class="chat-bubble right">${userMessage}</div>`;
                $msgTemplate.append(userMessageHTML);
                container.children('.chat-inner').append($msgTemplate);
                processUserMessage(userMessage);
                $('#user-message').val(''); // Clear the input field after sending the message
        }
    });

    function validateUserInput(csrfToken, field, userInput) {
        $.ajax({
            type: 'POST',
            url: '/input_validation/', // URL to the Django view
            data: {
                'validation_field' : field,
                'input_to_validate': userInput,
                'csrfmiddlewaretoken': csrfToken // CSRF token
            },
            success: function(response) {
                // response will contain 'True' or 'False' 
                console.log('Validation result:', response);
            },
            error: function(error) {
                console.log('Error:', error);
            }
        });
    }

}(jQuery));
