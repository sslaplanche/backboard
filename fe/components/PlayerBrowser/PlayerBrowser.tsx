import { createClient } from '@/utils/supabase/server'
import { cookies } from 'next/headers'
import FilterSearch from './FilterSearch'

const PlayerBrowser = async () => {

    const supabase = createClient(cookies())

    
    let { data, error } = await supabase
    .from('Player')
    .select('*')
            
    console.log(data)


    return (
        <>
            <FilterSearch rows={data} filterColumns={['first_name', 'last_name']} />
        </>
    )
}

export default PlayerBrowser;
