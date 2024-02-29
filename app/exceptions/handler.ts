import { errors } from '@adonisjs/auth'
import app from '@adonisjs/core/services/app'
import { HttpContext, ExceptionHandler } from '@adonisjs/core/http'

export default class HttpExceptionHandler extends ExceptionHandler {
  /**
   * In debug mode, the exception handler will display verbose errors
   * with pretty printed stack traces.
   */
  protected debug = !app.inProduction

  /**
   * The method is used for handling errors and returning
   * response to the client
   */
  async handle(error: unknown, ctx: HttpContext) {
    if (error instanceof errors.E_INVALID_CREDENTIALS) {
      return ctx.response.unprocessableEntity({ message: error.message })
    }

    if (error instanceof errors.E_UNAUTHORIZED_ACCESS) {
      return ctx.response.unauthorized({ message: error.message })
    }

    // @ts-ignore
    if (error.code === 'E_VALIDATION_ERROR') {
      const er = {
        status: 422,
        code: 'E_VALIDATION_ERROR',
        // @ts-ignore
        messages: error.messages.reduce((acc, curr) => {
          acc[curr.field] = curr.message
          return acc
        }, {}),
      }

      // @ts-ignore
      return super.handle(er, ctx)
    }

    return super.handle(error, ctx)
  }

  /**
   * The method is used to report error to the logging service or
   * the a third party error monitoring service.
   *
   * @note You should not attempt to send a response from this method.
   */
  async report(error: unknown, ctx: HttpContext) {
    return super.report(error, ctx)
  }
}
