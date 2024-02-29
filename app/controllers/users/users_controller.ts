import type { HttpContext } from '@adonisjs/core/http'

import User from '#models/user/index'
import { CreateUserValidator, UpdateUserValidator } from '#validators/user/user'

export default class UsersController {
  /**
   * Display a list of resource
   */
  async index({ request, response }: HttpContext) {
    const page = request.input('page', 1)
    const limit = request.input('limit', 10)

    const users = await User.query().paginate(page, limit)

    users.baseUrl('/users')

    return response.ok(users)
  }

  /**
   * Handle form submission for the create action
   */
  async store({ request, response }: HttpContext) {
    const payload = await request.validateUsing(CreateUserValidator)

    const user = await User.create(payload)

    return response.created(user)
  }

  /**
   * Show individual record
   */
  async show({ params, response }: HttpContext) {
    const user = await User.find(params.id)

    if (!user) {
      return response.notFound({ message: 'User not found' })
    }

    return response.ok(user)
  }

  /**
   * Update user record
   */
  async update({ params, request, response, auth }: HttpContext) {
    const user = await User.find(params.id)

    if (!user) {
      return response.notFound({ message: 'User not found' })
    }

    if (user.id !== auth.user!.id) {
      return response.forbidden({ message: 'Unauthorized access' })
    }

    const payload = await request.validateUsing(UpdateUserValidator, {
      meta: { userId: auth.user!.id },
    })

    user.merge(payload)

    await user.save()

    return response.ok(user)
  }
}
