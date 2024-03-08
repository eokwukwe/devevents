import vine from '@vinejs/vine'

/**
 * Validates the user's creation action
 */
export const CreateEventValidator = vine.compile(
  vine.object({
    title: vine.string().trim(),
    description: vine.string().trim(),
    attendee_total: vine.number({ strict: true }).min(1),
    venue: vine.string().trim(),
    date: vine.date().afterOrEqual('today'),
    category_id: vine.number({ strict: true }).exists(async (db, value, _field) => {
      const category = await db.from('categories').where('id', value).first()

      return category
    }),
  })
)
