import { createClient } from '@/utils/supabase/server'
import { cookies } from 'next/headers'


export default async function UserPlayers() {
    const supabase = createClient(cookies())
    const {
        data: { user },
    } = await supabase.auth.getUser()

    // Get all UserPlayer's for this user
    const { data: userPlayers, error } = await supabase.from('UserPlayer').select('*').eq('user_id', user.id)

    return (
        <>
            <p>
                Welcome, {user.email}!
            </p>
            { userPlayers? 
                <p>{JSON.stringify(userPlayers)}</p>
                :
                <p>WTF No players dummy?</p>
            }
        </>
    )

}