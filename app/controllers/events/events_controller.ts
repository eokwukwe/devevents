import { DateTime } from 'luxon'
import type { HttpContext } from '@adonisjs/core/http'

import Event from '#models/event/event'
import { CreateEventValidator } from '#validators/event/event'
import GoogleMapServices from '#services/google/google_map_services'

const serialize = {
  fields: {
    omit: ['user_id', 'category_id', 'created_at', 'updated_at'],
  },
  relations: {
    user: {
      fields: ['id', 'first_name', 'last_name', 'email', 'bio'],
    },
    attendees: {
      fields: ['id', 'first_name', 'last_name', 'bio'],
    },
  },
}

export default class EventsController {
  /**
   * Display a list of resource
   */
  async index({ request, response }: HttpContext) {
    const page = request.input('page', 1)
    const limit = request.input('limit', 10)

    const result = await Event.query()
      .preload('user')
      .preload('category')
      .preload('attendees')
      .paginate(page, limit)

    result.baseUrl('/events')

    const events = result.serialize(serialize)

    return response.ok(events)
  }

  /**
   * Handle form submission for the create action
   */
  async store({ request, response, auth }: HttpContext) {
    const payload = await request.validateUsing(CreateEventValidator)

    const latlng = await GoogleMapServices.getLatLng(payload.venue)

    const event = await Event.create({
      ...payload,
      date: DateTime.fromJSDate(new Date(payload.date)),
      userId: auth.user!.id,
      venueLat: latlng.lat,
      venueLng: latlng.lng,
    })

    await event.related('attendees').attach([auth.user!.id])

    return response.created(event)
  }

  /**
   * Show individual record
   */
  async show({ params, response }: HttpContext) {
    const result = await Event.query()
      .where('id', params.id)
      .preload('user')
      .preload('category')
      .preload('attendees')
      .firstOrFail()

    const event = result.serialize(serialize)

    return response.ok(event)
  }

  /**
   * Handle form submission for the edit action
   */
  async update({ params, request, response, auth }: HttpContext) {
    const event = await Event.findOrFail(params.id)

    if (event.userId !== auth.user!.id) {
      return response.forbidden({ message: 'Unauthorized access' })
    }

    const payload = await request.validateUsing(CreateEventValidator)

    const latlng = await GoogleMapServices.getLatLng(payload.venue)

    event
      .merge({
        ...payload,
        date: DateTime.fromJSDate(new Date(payload.date)),
        venueLat: latlng.lat,
        venueLng: latlng.lng,
      })
      .save()

    return response.ok(event)
  }

  /**
   * Delete record
   */
  async destroy({ params, auth, response }: HttpContext) {
    const event = await Event.findOrFail(params.id)

    if (event.userId !== auth.user!.id) {
      return response.forbidden({ message: 'Unauthorized access' })
    }

    await event.delete()

    return response.noContent()
  }
}
