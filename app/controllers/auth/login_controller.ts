import { HttpContext } from '@adonisjs/core/http'

import User from '#models/user/index'
import { LoginValidator } from '#validators/user/user'

export default class LoginController {
  async handle({ request, response }: HttpContext) {
    const { email, password } = await request.validateUsing(LoginValidator)

    const user = await User.verifyCredentials(email, password)

    const token = await User.accessTokens.create(user)

    return response.ok({
      token_type: 'bearer',
      access_token: token.value!.release(),
    })
  }
}
