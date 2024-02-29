import vine from '@vinejs/vine'

/**
 * Validates the user's creation action
 */
export const CreateUserValidator = vine.compile(
  vine.object({
    first_name: vine.string().trim(),
    last_name: vine.string().trim(),
    email: vine
      .string()
      .email()
      .unique(async (db, value, _field) => {
        return !(await db.from('users').where('email', value).first())
      }),
    password: vine.string().minLength(8).maxLength(32).trim(),
  })
)

/**
 * Validates the user's update action
 */
export const UpdateUserValidator = vine.compile(
  vine.object({
    first_name: vine.string().trim(),
    last_name: vine.string().trim(),
    email: vine
      .string()
      .email()
      .unique(async (db, value, field) => {
        const user = await db
          .from('users')
          .whereNot('id', field.meta.userId)
          .where('email', value)
          .first()

        return !user
      }),
    bio: vine.string().trim(),
  })
)

/**
 * Validates user password update
 */
export const UpdatePasswordValidator = vine.compile(
  vine.object({
    old_password: vine.string().trim(),
    new_password: vine.string().minLength(8).maxLength(32).trim(),
  })
)

/**
 * Validates the user's login action
 */
export const LoginValidator = vine.compile(
  vine.object({
    email: vine.string().email(),
    password: vine.string().trim(),
  })
)
