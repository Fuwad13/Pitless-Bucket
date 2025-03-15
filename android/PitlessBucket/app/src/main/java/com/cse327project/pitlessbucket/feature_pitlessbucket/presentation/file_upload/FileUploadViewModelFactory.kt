package com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.file_upload

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard.ApiService

class FileUploadViewModelFactory(private val apiService: ApiService) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return FileUploadViewModel(apiService) as T
    }
}
