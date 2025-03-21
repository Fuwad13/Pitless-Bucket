package com.cse327project.pitlessbucket.file_manager.presentation.dashboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.cse327project.pitlessbucket.core.data.data_source.ApiService

class DashboardViewModelFactory(private val apiService: ApiService) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return DashboardViewModel(apiService) as T
    }
}