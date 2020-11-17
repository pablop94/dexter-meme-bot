#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.


import os

from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from image import crear_meme_desde_archivo, agregar_texto
from settings import TEMP_FOLDER
from log import logger



def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hola, soy el bot para crear el meme de Dexter")
    enviar_ayuda(update)


def enviar_ayuda(update):
    update.message.reply_text(
        """*Modo de uso*
        - Enviar una imagen: Arma el meme con la imagen enviada.
        - Enviar una imagen con comentario: el comentario aparece en un cuadro blanco arriba del meme. Arma el meme con la imagen enviada.
        -Enviar Sticker no animado: Arma el meme con el sticker enviado.

        Para ver este mensaje nuevamente manda /ayuda.
        """, 
        parse_mode=ParseMode.MARKDOWN)

def comando_ayuda(update: Update, context: CallbackContext) -> None:
    enviar_ayuda(update)

def procesar_imagen(photo_file, filepath, filename):
    photo_file.download(filepath)
    
    return crear_meme_desde_archivo(filepath)

def borrar_imagenes(*paths):
    for path in paths:
        os.remove(path)


def crear_meme(update: Update, context: CallbackContext) -> None:
    filename = f'user_photo{update.message.message_id}.jpg'
    filepath = f'{TEMP_FOLDER}{filename}'
    result_path = f'{TEMP_FOLDER}result_{filename}.png'
    logger.info('hola request')
    update.message.reply_text('Dame un cacho...')

    if len(update.message.photo) >= 1:
        image = procesar_imagen(update.message.photo[-1].get_file(), filepath, filename)

    elif update.message.sticker is not None:
        if update.message.sticker.is_animated:
            raise Exception('animated_sticker')

        image = procesar_imagen(update.message.sticker.get_file(), filepath, filename)

    if update.message.caption is not None:
        image = agregar_texto(update.message.caption, image)

    image.save(result_path)

    with open(result_path, 'rb') as img:
        update.message.reply_photo(img)

    borrar_imagenes(filepath, result_path)

def error_handler(update: Update, context: CallbackContext) -> None:
    if str(context.error) == 'animated_sticker':
        logger.error('Animated sticker received')
        update.message.reply_text('No se permiten stickers animados')
        update.message.reply_text('todavía...')
        update.message.reply_text('pero el futuro es incierto')
    else:
        logger.error(str(context.error))

def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("ayuda", comando_ayuda))

    dispatcher.add_handler(MessageHandler(Filters.photo | Filters.sticker | Filters.caption, crear_meme))
    dispatcher.add_error_handler(error_handler)

def run_bot():
    updater = Updater(os.environ["TELEGRAM_TOKEN"])

    dispatcher = updater.dispatcher

    register_handlers(dispatcher)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run_bot()
