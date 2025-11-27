/**
 * Utility composable for common formatting functions
 */
export const useFormatters = () => {
    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        })
    }

    const formatLongDate = (dateString: string) => {
        const date = new Date(dateString)
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        })
    }

    const formatPrice = (price: number) => {
        return `$${price.toFixed(2)}`
    }

    const getStatusColor = (status: string) => {
        switch (status?.toLowerCase()) {
            case 'confirmed':
                return 'success'
            case 'cancelled':
                return 'error'
            case 'pending':
                return 'warning'
            case 'active':
                return 'info'
            default:
                return 'grey'
        }
    }

    const formatSeatLabel = (rowNumber: number, seatNumber: number) => {
        return `R${rowNumber}S${seatNumber}`
    }

    const truncateText = (text: string, maxLength: number = 100) => {
        if (text.length <= maxLength) return text
        return text.substring(0, maxLength) + '...'
    }

    return {
        formatDate,
        formatLongDate,
        formatPrice,
        getStatusColor,
        formatSeatLabel,
        truncateText
    }
}