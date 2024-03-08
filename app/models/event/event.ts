import { DateTime } from 'luxon'
import { BaseModel, belongsTo, column, manyToMany } from '@adonisjs/lucid/orm'
import type { BelongsTo, ManyToMany } from '@adonisjs/lucid/types/relations'

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
  declare coverImage: string | null

  @column()
  declare venue: string

  @column()
  declare attendeeTotal: number

  @column()
  declare venueLat: number

  @column()
  declare venueLng: number

  @column.dateTime()
  declare date: DateTime

  @column()
  declare userId: number

  @column()
  declare categoryId: number

  @column.dateTime({ autoCreate: true })
  declare createdAt: DateTime

  @column.dateTime({ autoCreate: true, autoUpdate: true })
  declare updatedAt: DateTime

  @belongsTo(() => User)
  declare user: BelongsTo<typeof User>

  @belongsTo(() => Category)
  declare category: BelongsTo<typeof Category>

  @manyToMany(() => User, {
    localKey: 'id',
    relatedKey: 'id',
    pivotForeignKey: 'event_id',
    pivotTable: 'event_attendees',
    pivotRelatedForeignKey: 'user_id',
  })
  declare attendees: ManyToMany<typeof User>
}
