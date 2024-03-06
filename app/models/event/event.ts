import { DateTime } from 'luxon'
import { BaseModel, belongsTo, column } from '@adonisjs/lucid/orm'
import type { BelongsTo } from '@adonisjs/lucid/types/relations'

import User from '#models/user/index'
import Category from '#models/event/category'

export default class Event extends BaseModel {
  @column({ isPrimary: true })
  declare id: number

  @column()
  declare title: string

  @column()
  declare description: string

  @column()
  declare cover_image: string | null

  @column()
  declare venue: string

  @column()
  declare attendee_total: number

  @column()
  declare venue_lat: number

  @column()
  declare venue_lng: number

  @column.dateTime()
  declare date: DateTime

  @column()
  declare user_id: number

  @column()
  declare category_id: number

  @column.dateTime({ autoCreate: true })
  declare createdAt: DateTime

  @column.dateTime({ autoCreate: true, autoUpdate: true })
  declare updatedAt: DateTime

  @belongsTo(() => User)
  declare user: BelongsTo<typeof User>

  @belongsTo(() => Category)
  declare category: BelongsTo<typeof Category>
}
