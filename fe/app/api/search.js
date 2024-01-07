import { cookies } from 'next/headers'
import { createClient } from '@/utils/supabase/server'

const supabase = createClient(cookies())

export default async function handler(req, res) {
    const { query } = req.query

    try {
        const { data, error } = await supabase
            .from('Player')
            .select('*')
            .ilike('last_name', `%${query}%`)
        
        if (error) {
            console.log(error)
            return res.status(500).json({ error: error.message })
        }

        console.log(data)
        res.status(200).json(data)
    } catch (error) {
        console.log(error)
        res.status(500).json({ error: error.message })
    }
}
